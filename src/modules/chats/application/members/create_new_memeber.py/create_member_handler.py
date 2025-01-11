from ....domain.members.interfaces.repository import AbstractMemberRepository
from ....domain.members.root import Member
from ....domain.members.value_objects.member_id import MemberId
from ...configuration.command_handler import AbstractCommandHandler
from .create_member_command import CreateMemberCommand


class CreateMemberCommandHandler(AbstractCommandHandler[CreateMemberCommand, Member]):
    def __init__(self, member_repository: AbstractMemberRepository):
        self._member_repository = member_repository

    def handle(self, command: CreateMemberCommand) -> Member:
        # Create member ID value object
        member_id = MemberId(value=command.member_id)

        # Create the member entity
        member = Member.create(
            id=member_id,
            first_name=command.first_name,
            last_name=command.last_name,
            is_admin=command.is_admin,
            is_creator=command.is_creator,
        )

        # Save the member to the repository
        self._member_repository.save(member)

        return member
