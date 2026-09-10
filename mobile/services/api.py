import requests


class APIService:

    def __init__(self):

        self.supabase_url = (
            "YOUR_SUPABASE_URL"
        )

        self.supabase_key = (
            "YOUR_SUPABASE_ANON_KEY"
        )

        self.session = None



    def login(
        self,
        national_code,
        password
    ):

        """
        ورود کاربر از طریق Supabase Auth

        مسیر:
        کد ملی → ایمیل → Auth Login
        """

        try:

            email = self.get_user_email(
                national_code
            )


            if not email:

                print(
                    "EMAIL NOT FOUND"
                )

                return None



            url = (
                self.supabase_url
                +
                "/auth/v1/token?grant_type=password"
            )


            headers = {

                "apikey":
                    self.supabase_key,

                "Content-Type":
                    "application/json"

            }


            data = {

                "email":
                    email,

                "password":
                    password

            }


            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=15
            )


            print(
                "LOGIN STATUS:",
                response.status_code
            )


            if response.status_code != 200:

                print(
                    response.text
                )

                return None



            result = response.json()



            return {

                "access_token":
                    result.get(
                        "access_token"
                    ),

                "refresh_token":
                    result.get(
                        "refresh_token"
                    ),

                "user":
                    result.get(
                        "user"
                    )

            }


        except Exception as exc:

            print(
                "API LOGIN ERROR:",
                exc
            )

            return None




    def get_user_email(
        self,
        national_code
    ):

        """
        پیدا کردن ایمیل کاربر
        با کد ملی
        """

        try:

            url = (
                self.supabase_url
                +
                "/rest/v1/users"
                +
                "?national_code=eq."
                +
                national_code
            )


            headers = {

                "apikey":
                    self.supabase_key,

                "Authorization":
                    "Bearer "
                    +
                    self.supabase_key

            }


            response = requests.get(
                url,
                headers=headers,
                timeout=15
            )


            if response.status_code != 200:

                print(
                    response.text
                )

                return None



            users = response.json()


            if not users:

                return None



            return users[0].get(
                "email"
            )



        except Exception as exc:

            print(
                "EMAIL ERROR:",
                exc
            )

            return None
