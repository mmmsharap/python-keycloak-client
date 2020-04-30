import json
from collections import OrderedDict

from keycloak.admin import KeycloakAdminBase, KeycloakAdminEntity
from .clientroles import to_camel_case

ROLE_KWARGS = [
    'description',
    'id',
    'realm_role',
    'composite',
    'composites',
    'container_id',
    'scope_param_required'
]

__all__ = ('RealmRole', 'RealmRoles',)


class RealmRoles(KeycloakAdminBase):
    _realm_name = None
    _paths = {
        'collection': '/auth/admin/realms/{realm}/roles'
    }

    def __init__(self, realm_name, *args, **kwargs):
        self._realm_name = realm_name
        super(RealmRoles, self).__init__(*args, **kwargs)

    def all(self):
        return self._client.get(
            self._client.get_full_url(
                self.get_path('collection', realm=self._realm_name)
            )
        )

    def by_name(self, role_name):
        return RealmRole(realm_name=self._realm_name,
                         role_name=role_name, client=self._client)

    def create(self, name, **kwargs):
        """
        Create realm role
        """
        payload = OrderedDict(name=name)

        for key in ROLE_KWARGS:
            if key in kwargs:
                payload[to_camel_case(key)] = kwargs[key]

        return self._client.post(
            url=self._client.get_full_url(
                self.get_path('collection',
                              realm=self._realm_name,
                              )
            ),
            data=json.dumps(payload, sort_keys=True)
        )


class RealmRole(KeycloakAdminEntity):
    _paths = {
        'single': '/auth/admin/realms/{realm}/roles/{role_name}'
    }

    def __init__(self, realm_name, role_name, client):
        self._realm_name = realm_name
        self._role_name = role_name

        super(RealmRole, self).__init__(
            url=self.get_path("single", realm=realm_name, role_name=role_name),
            client=client)
