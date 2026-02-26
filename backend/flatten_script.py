import os
import shutil
from pathlib import Path

backend_dir = Path("/Users/nicolaibrahim/Desktop/proj/Bot-Chating/backend")

moves = [
    # Accounts
    (
        "src/modules/accounts/application/access_control/assign_role/command.py",
        "src/modules/accounts/application/access_control/assign_role_command.py",
    ),
    (
        "src/modules/accounts/application/access_control/assign_role/dto.py",
        "src/modules/accounts/application/access_control/assign_role_dto.py",
    ),
    (
        "src/modules/accounts/application/account/get_account/query.py",
        "src/modules/accounts/application/account/get_account_query.py",
    ),
    (
        "src/modules/accounts/application/account/list_accounts/query.py",
        "src/modules/accounts/application/account/list_accounts_query.py",
    ),
    (
        "src/modules/accounts/application/account/remove_account/command.py",
        "src/modules/accounts/application/account/remove_account_command.py",
    ),
    (
        "src/modules/accounts/application/account/update_account/command.py",
        "src/modules/accounts/application/account/update_account_command.py",
    ),
    (
        "src/modules/accounts/application/account/verify_account/command.py",
        "src/modules/accounts/application/account/verify_account_command.py",
    ),
    (
        "src/modules/accounts/application/authentication/issue_token/command.py",
        "src/modules/accounts/application/authentication/issue_token_command.py",
    ),
    (
        "src/modules/accounts/application/authentication/issue_token/dto.py",
        "src/modules/accounts/application/authentication/issue_token_dto.py",
    ),
    (
        "src/modules/accounts/application/authentication/login/command.py",
        "src/modules/accounts/application/authentication/login_command.py",
    ),
    (
        "src/modules/accounts/application/authentication/login/dto.py",
        "src/modules/accounts/application/authentication/login_dto.py",
    ),
    (
        "src/modules/accounts/application/authentication/logout/command.py",
        "src/modules/accounts/application/authentication/logout_command.py",
    ),
    (
        "src/modules/accounts/application/registration/register_account/command.py",
        "src/modules/accounts/application/registration/register_account_command.py",
    ),
    (
        "src/modules/accounts/application/registration/register_account/dto.py",
        "src/modules/accounts/application/registration/register_account_dto.py",
    ),
    # Chats
    (
        "src/modules/chats/application/conversation_lifecycle/archive_conversation/command.py",
        "src/modules/chats/application/conversation_lifecycle/archive_conversation_command.py",
    ),
    (
        "src/modules/chats/application/conversation_lifecycle/rename_conversation/command.py",
        "src/modules/chats/application/conversation_lifecycle/rename_conversation_command.py",
    ),
    (
        "src/modules/chats/application/conversation_lifecycle/start_conversation/command.py",
        "src/modules/chats/application/conversation_lifecycle/start_conversation_command.py",
    ),
    (
        "src/modules/chats/application/conversation_lifecycle/start_conversation/dto.py",
        "src/modules/chats/application/conversation_lifecycle/start_conversation_dto.py",
    ),
    (
        "src/modules/chats/application/membership/add_member/command.py",
        "src/modules/chats/application/membership/add_member_command.py",
    ),
    (
        "src/modules/chats/application/membership/change_member_role/command.py",
        "src/modules/chats/application/membership/change_member_role_command.py",
    ),
    (
        "src/modules/chats/application/membership/remove_member/command.py",
        "src/modules/chats/application/membership/remove_member_command.py",
    ),
    (
        "src/modules/chats/application/messaging/delete_message/command.py",
        "src/modules/chats/application/messaging/delete_message_command.py",
    ),
    (
        "src/modules/chats/application/messaging/edit_message/command.py",
        "src/modules/chats/application/messaging/edit_message_command.py",
    ),
    (
        "src/modules/chats/application/messaging/send_message/command.py",
        "src/modules/chats/application/messaging/send_message_command.py",
    ),
    (
        "src/modules/chats/application/messaging/send_message/dto.py",
        "src/modules/chats/application/messaging/send_message_dto.py",
    ),
    (
        "src/modules/chats/application/queries/get_conversation_details/dto.py",
        "src/modules/chats/application/queries/get_conversation_details_dto.py",
    ),
    (
        "src/modules/chats/application/queries/get_conversation_details/query.py",
        "src/modules/chats/application/queries/get_conversation_details_query.py",
    ),
    (
        "src/modules/chats/application/queries/list_messages/dto.py",
        "src/modules/chats/application/queries/list_messages_dto.py",
    ),
    (
        "src/modules/chats/application/queries/list_messages/query.py",
        "src/modules/chats/application/queries/list_messages_query.py",
    ),
    (
        "src/modules/chats/application/queries/list_user_conversations/dto.py",
        "src/modules/chats/application/queries/list_user_conversations_dto.py",
    ),
    (
        "src/modules/chats/application/queries/list_user_conversations/query.py",
        "src/modules/chats/application/queries/list_user_conversations_query.py",
    ),
    # LLM Backend
    (
        "src/modules/llm_backend/application/generation/generate_response/generate_response_command.py",
        "src/modules/llm_backend/application/generation/generate_response_command.py",
    ),
    (
        "src/modules/llm_backend/application/tokenization/tokenize_text/tokenize_text_command.py",
        "src/modules/llm_backend/application/tokenization/tokenize_text_command.py",
    ),
]

dirs_to_remove = set()

for src, dest in moves:
    src_path = backend_dir / src
    dest_path = backend_dir / dest

    if src_path.exists():
        shutil.move(src_path, dest_path)
        print(f"Moved {src_path.name} -> {dest_path.name}")
    elif dest_path.exists():
        print(f"Already moved {dest_path.name}")
    else:
        print(f"NOT FOUND: {src}")

    dirs_to_remove.add(src_path.parent)

for d in dirs_to_remove:
    if d.exists() and d.is_dir():
        shutil.rmtree(d)
        print(f"Removed directory {d.name}")
