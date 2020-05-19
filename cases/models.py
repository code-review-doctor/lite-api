import uuid
from collections import defaultdict

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from audit_trail.enums import AuditType
from cases.enums import (
    AdviceType,
    CaseDocumentState,
    CaseTypeTypeEnum,
    CaseTypeSubTypeEnum,
    CaseTypeReferenceEnum,
    ECJUQueryType,
    AdviceLevel,
)
from cases.libraries.reference_code import generate_reference_code
from cases.managers import CaseManager, CaseReferenceCodeManager, AdviceManager
from common.models import TimestampableModel
from documents.models import Document
from flags.models import Flag
from goods.enums import PvGrading
from organisations.models import Organisation
from queues.models import Queue
from static.countries.models import Country
from static.denial_reasons.models import DenialReason
from static.statuses.enums import CaseStatusEnum
from static.statuses.libraries.get_case_status import get_case_status_by_status
from static.statuses.models import CaseStatus
from teams.models import Team
from users.models import (
    BaseUser,
    ExporterUser,
    GovUser,
    UserOrganisationRelationship,
    ExporterNotification,
)


class CaseType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(choices=CaseTypeTypeEnum.choices, null=False, blank=False, max_length=35)
    sub_type = models.CharField(choices=CaseTypeSubTypeEnum.choices, null=False, blank=False, max_length=35)
    reference = models.CharField(
        choices=CaseTypeReferenceEnum.choices, unique=True, null=False, blank=False, max_length=5,
    )


class Case(TimestampableModel):
    """
    Base model for applications and queries
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_code = models.CharField(max_length=30, unique=True, null=True, blank=False, editable=False, default=None)
    case_type = models.ForeignKey(CaseType, on_delete=models.DO_NOTHING, null=False, blank=False)
    queues = models.ManyToManyField(Queue, related_name="cases")
    flags = models.ManyToManyField(Flag, related_name="cases")
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey(
        CaseStatus, related_name="query_status", on_delete=models.CASCADE, blank=True, null=True,
    )
    case_officer = models.ForeignKey(GovUser, null=True, on_delete=models.DO_NOTHING)
    copy_of = models.ForeignKey("self", default=None, null=True, on_delete=models.DO_NOTHING)
    last_closed_at = models.DateTimeField(null=True)

    sla_days = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    sla_remaining_days = models.SmallIntegerField(null=True)
    sla_updated_at = models.DateTimeField(null=True)

    objects = CaseManager()

    def save(self, *args, **kwargs):
        if CaseStatusEnum.is_terminal(self.status.status):
            self.case_officer = None
            self.queues.clear()
            CaseAssignment.objects.filter(case=self).delete()

        if not self.reference_code and self.status != get_case_status_by_status(CaseStatusEnum.DRAFT):
            self.reference_code = generate_reference_code(self)

        super(Case, self).save(*args, **kwargs)

    def get_case(self):
        """
        For any child models, this method allows easy access to the parent Case.

        Child cases [StandardApplication, OpenApplication, ...] share `id` with Case.
        """
        if type(self) == Case:
            return self

        return Case.objects.get(id=self.id)

    def get_users(self):
        case_assignments = self.case_assignments.select_related("queue", "user").order_by("queue__name")
        return_value = defaultdict(list)

        for assignment in case_assignments:
            return_value[assignment.queue.name].append(
                {
                    "id": assignment.user.id,
                    "first_name": assignment.user.first_name,
                    "last_name": assignment.user.last_name,
                }
            )

        return return_value

    def parameter_set(self):
        """
        This function looks at the case determines the flags, casetype, and countries of that case,
            and puts these objects into a set
        :return: set object
        """
        from applications.models import PartyOnApplication
        from applications.models import GoodOnApplication
        from applications.models import CountryOnApplication
        from goodstype.models import GoodsType

        parameter_set = set(self.flags.all()) | {self.case_type} | set(self.organisation.flags.all())

        for poa in PartyOnApplication.objects.filter(application=self.id):
            parameter_set = (
                parameter_set | {poa.party.country} | set(poa.party.flags.all()) | set(poa.party.country.flags.all())
            )

        for goa in GoodOnApplication.objects.filter(application=self.id):
            parameter_set = parameter_set | set(goa.good.flags.all())

        for goods_type in GoodsType.objects.filter(application=self.id):
            parameter_set = parameter_set | set(goods_type.flags.all())

        for coa in CountryOnApplication.objects.filter(application=self.id):
            parameter_set = parameter_set | {coa.country} | set(coa.country.flags.all())

        return parameter_set

    def remove_all_case_assignments(self):
        """
        Will look at a case, and should the case contain any queue or user assignments will remove assignments, and
            audit the removal of said assignments against the case.
        """
        from audit_trail import service as audit_trail_service

        case = self.get_case()
        assigned_cases = CaseAssignment.objects.filter(case=case)

        if self.queues.exists():
            self.queues.clear()

            audit_trail_service.create_system_user_audit(
                verb=AuditType.REMOVE_CASE_FROM_ALL_QUEUES, action_object=case,
            )

        if assigned_cases.exists():
            assigned_cases.delete()

            audit_trail_service.create_system_user_audit(
                verb=AuditType.REMOVE_CASE_FROM_ALL_USER_ASSIGNMENTS, action_object=case,
            )


class CaseReferenceCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_number = models.IntegerField()
    year = models.IntegerField(editable=False, unique=True)

    objects = CaseReferenceCodeManager()


class CaseNote(TimestampableModel):
    """
    Note on a case, visible to internal users and exporters depending on is_visible_to_exporter.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, related_name="case_note", on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, related_name="case_note", on_delete=models.CASCADE, default=None, null=False,)
    text = models.TextField(default=None, blank=True, null=True, max_length=2200)
    is_visible_to_exporter = models.BooleanField(default=False, blank=False, null=False)

    notifications = GenericRelation(ExporterNotification, related_query_name="case_note")

    def save(self, *args, **kwargs):
        exporter_user = False
        if isinstance(self.user, ExporterUser) or ExporterUser.objects.filter(id=self.user.id).exists():
            self.is_visible_to_exporter = True
            exporter_user = True

        send_notification = not exporter_user and self.is_visible_to_exporter and self._state.adding
        super(CaseNote, self).save(*args, **kwargs)

        if send_notification:
            for user_relationship in UserOrganisationRelationship.objects.filter(organisation=self.case.organisation):
                user_relationship.send_notification(content_object=self, case=self.case)


class CaseAssignment(TimestampableModel):
    """
    Assigns users to a case on a particular queue
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="case_assignments")
    user = models.ForeignKey(GovUser, on_delete=models.CASCADE, related_name="case_assignments")
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name="case_assignments")

    class Meta:
        unique_together = [["case", "user", "queue"]]

    def save(self, *args, **kwargs):
        from audit_trail import service as audit_trail_service

        audit_user = None

        if "audit_user" in kwargs:
            audit_user = kwargs.pop("audit_user")

        super(CaseAssignment, self).save(*args, **kwargs)
        if audit_user:
            audit_trail_service.create(
                actor=audit_user,
                verb=AuditType.ASSIGN_CASE,
                action_object=self.case,
                payload={"assignment": f"{self.user.first_name} {self.user.last_name}"},
            )


class CaseDocument(Document):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    user = models.ForeignKey(GovUser, on_delete=models.CASCADE)
    description = models.TextField(default=None, blank=True, null=True, max_length=280)
    type = models.CharField(
        choices=CaseDocumentState.choices, default=CaseDocumentState.UPLOADED, max_length=100, null=False
    )
    visible_to_exporter = models.BooleanField(blank=False, null=False)


class Advice(TimestampableModel):
    """
    Advice for goods and destinations on cases
    """

    ENTITY_FIELDS = ["good", "goods_type", "country", "end_user", "consignee", "ultimate_end_user", "third_party"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, related_name="advice", on_delete=models.CASCADE)
    user = models.ForeignKey(GovUser, on_delete=models.PROTECT)
    type = models.CharField(choices=AdviceType.choices, max_length=30)
    text = models.TextField(default=None, blank=True, null=True)
    note = models.TextField(default=None, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    level = models.CharField(choices=AdviceLevel.choices, max_length=30)

    # optional footnotes for advice
    footnote = models.TextField(blank=True, null=True, default=None)
    footnote_required = models.BooleanField(null=True, blank=True, default=None)

    # Optional goods/destinations
    good = models.ForeignKey("goods.Good", related_name="advice", on_delete=models.CASCADE, null=True)
    goods_type = models.ForeignKey("goodstype.GoodsType", related_name="advice", on_delete=models.CASCADE, null=True)
    country = models.ForeignKey("countries.Country", related_name="advice", on_delete=models.CASCADE, null=True)
    end_user = models.ForeignKey("parties.Party", on_delete=models.CASCADE, null=True)
    ultimate_end_user = models.ForeignKey(
        "parties.Party", on_delete=models.CASCADE, related_name="ultimate_end_user", null=True
    )
    consignee = models.ForeignKey("parties.Party", on_delete=models.CASCADE, related_name="consignee", null=True)
    third_party = models.ForeignKey("parties.Party", on_delete=models.CASCADE, related_name="third_party", null=True)

    # Optional depending on type of advice
    proviso = models.TextField(default=None, blank=True, null=True)
    denial_reasons = models.ManyToManyField(DenialReason)
    pv_grading = models.CharField(choices=PvGrading.choices, null=True, max_length=30)
    # This is to store the collated security grading(s) for display purposes
    collated_pv_grading = models.TextField(default=None, blank=True, null=True)

    objects = AdviceManager()

    class Meta:
        db_table = "advice"

    @property
    def entity_field(self):
        for field in self.ENTITY_FIELDS:
            entity = getattr(self, field, None)
            if entity:
                return field

    @property
    def entity(self):
        return getattr(self, self.entity_field, None)

    def save(self, *args, **kwargs):
        if self.type != AdviceType.PROVISO and self.type != AdviceType.CONFLICTING:
            self.proviso = None
        try:
            if self.level == AdviceLevel.TEAM:
                Advice.objects.get(
                    case=self.case,
                    team=self.team,
                    level=AdviceLevel.TEAM,
                    good=self.good,
                    goods_type=self.goods_type,
                    country=self.country,
                    end_user=self.end_user,
                    ultimate_end_user=self.ultimate_end_user,
                    consignee=self.consignee,
                    third_party=self.third_party,
                ).delete()
            elif self.level == AdviceLevel.FINAL:
                old_advice = Advice.objects.get(
                    case=self.case,
                    good=self.good,
                    level=AdviceLevel.FINAL,
                    goods_type=self.goods_type,
                    country=self.country,
                    end_user=self.end_user,
                    ultimate_end_user=self.ultimate_end_user,
                    consignee=self.consignee,
                    third_party=self.third_party,
                )
                self.footnote = old_advice.footnote
                self.footnote_required = old_advice.footnote_required
                old_advice.delete()
            elif self.level == AdviceLevel.USER:
                Advice.objects.get(
                    case=self.case,
                    good=self.good,
                    user=self.user,
                    level=AdviceLevel.USER,
                    goods_type=self.goods_type,
                    country=self.country,
                    end_user=self.end_user,
                    ultimate_end_user=self.ultimate_end_user,
                    consignee=self.consignee,
                    third_party=self.third_party,
                ).delete()
        except Advice.DoesNotExist:
            pass

        super(Advice, self).save(*args, **kwargs)

    def equals(self, other):
        return all(
            [
                self.type == other.type,
                self.text == other.text,
                self.note == other.note,
                self.proviso == other.proviso,
                self.pv_grading == other.pv_grading,
                [x for x in self.denial_reasons.values_list()] == [x for x in other.denial_reasons.values_list()],
            ]
        )


class EcjuQuery(TimestampableModel):
    """
    Query from ECJU to exporters
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(null=False, blank=False, max_length=5000)
    response = models.CharField(null=True, blank=False, max_length=2200)
    case = models.ForeignKey(Case, related_name="case_ecju_query", on_delete=models.CASCADE)
    responded_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    raised_by_user = models.ForeignKey(
        GovUser, related_name="govuser_ecju_query", on_delete=models.CASCADE, default=None, null=False,
    )
    responded_by_user = models.ForeignKey(
        ExporterUser, related_name="exportuser_ecju_query", on_delete=models.CASCADE, default=None, null=True,
    )
    query_type = models.CharField(
        choices=ECJUQueryType.choices, max_length=50, default=ECJUQueryType.ECJU, null=False, blank=False
    )

    notifications = GenericRelation(ExporterNotification, related_query_name="ecju_query")

    def save(self, *args, **kwargs):
        existing_instance_count = EcjuQuery.objects.filter(id=self.id).count()

        # Only create a notification when saving a ECJU query for the first time
        if existing_instance_count == 0:
            super(EcjuQuery, self).save(*args, **kwargs)
            for user_relationship in UserOrganisationRelationship.objects.filter(organisation=self.case.organisation):
                user_relationship.send_notification(content_object=self, case=self.case)
        else:
            self.responded_at = timezone.now()
            super(EcjuQuery, self).save(*args, **kwargs)


class GoodCountryDecision(TimestampableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    good = models.ForeignKey("goodstype.GoodsType", on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    decision = models.CharField(choices=AdviceType.choices, max_length=30)

    def save(self, *args, **kwargs):
        GoodCountryDecision.objects.filter(case=self.case, good=self.good, country=self.country).delete()

        super(GoodCountryDecision, self).save(*args, **kwargs)


class EnforcementCheckID(models.Model):
    """
    Enforcement XML doesn't support 64 bit ints (UUID's).
    So this mapping table maps entity uuid's to enforcement ids (32 bit)
    """

    id = models.AutoField(primary_key=True)
    entity_id = models.UUIDField(unique=True)
