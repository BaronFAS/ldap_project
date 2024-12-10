from accounts.models import User


def get_my_user(*, user: User):
    company_id = None
    company_name = None
    if user.company:
        company_id = user.company.id
        company_name = user.company.name
    response = {
        "id": user.id,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "company": company_name,
        "companyId": company_id,
        "phoneNumber": user.phone_number,
    }
    return response


def jwt_response_payload_handler(token, user=None, request=None):
    return {"token": token, "me": get_my_user(user=user)}


def get_user_permissions(permissions, user: User):
    has_permissions = {permission: user.has_perm(permission) for permission in permissions}
    return has_permissions
