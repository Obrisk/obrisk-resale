import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_pay_order_view(client):
    response = client.post(reverse("classifieds:wxpyjs_success"),
                                {"addr": "",
                                 "sg": "admin-red-lockers",
                                 "phone": "13289876516"
                                }
                            )
    content = response.content.decode(response.charset)
    assert response.status_code == 302
