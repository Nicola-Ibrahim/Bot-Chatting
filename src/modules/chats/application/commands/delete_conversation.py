def delete(self, conversation_id: uuid.UUID) -> Result:
    """
    Deletes a conversation session from the repository.

    Args:
        conversation_id (uuid.UUID): The unique ID of the conversation to delete.

    Returns:
        Result: A Result indicating the outcome of the delete operation.
    """
    try:
        conversation = self._repository.get_by_id(conversation_id)
        if not conversation:
            return Result.fail(RepositoryException.entity_not_found("Conversation not found."))

        self._repository.delete(conversation_id)
        return Result.ok(None)
    except BusinessRuleValidationException as e:
        return Result.fail(e)
