from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

# Check if user is staff
def staff_member_required(view_func):
    return user_passes_test(
        lambda u: u.is_staff,  # Test to check if user is staff
        login_url='dashboard-login'     # Redirect to the login page if not
    )(view_func)
