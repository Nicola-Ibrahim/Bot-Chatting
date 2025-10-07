class UserFactory:
    def create(type: str, data: dict):
        match type:
            case "admin":
                AdminUser(data)

            case "moderator":
                ModeratroUser(data)

            case "regular":
                RegularUser(data)
