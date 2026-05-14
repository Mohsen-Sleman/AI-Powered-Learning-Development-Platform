from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter) :
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        data = sociallogin.account.extra_data

        if sociallogin.account.provider == 'google' :
            full_name = data.get('name') or f"{data.get('given_name','')} {data.get('family_name','')}"
        elif sociallogin.account.provider == 'github' :
            full_name = data.get('name') or data.get('login')


        user.full_name = full_name.strip()
        user.is_verified = True 
        user.save()
        return user