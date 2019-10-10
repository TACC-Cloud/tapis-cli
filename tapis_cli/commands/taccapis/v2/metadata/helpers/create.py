from tapis_cli.utils import serializable


def __to_cu_data(name, value, validate=True):
    cu_data = {'name': None, 'value': None}

    # Handle cases where value is under 'value' AND generic JSON blob
    if isinstance(value, dict):
        val_val = value.get('value', value)
        cu_data['value'] = val_val
    else:
        cu_data['value'] = value

    # Allow 'name' to be passed via the JSON object rather than as an option
    if name is None and value.get('name', None) is not None:
        name = value.get('name')
    if name is None:
        raise ValueError('No value for "name" was provided')
    else:
        cu_data['name'] = name

    # Double check that the new metadata record is serializable to JSON
    try:
        serializable(cu_data, permissive=False)
    except Exception:
        raise

    return cu_data


def create_update(name=None,
                  value=None,
                  uuid=None,
                  peristent_name=False,
                  permissive=False,
                  agave=None):
    try:
        if peristent_name is True and name is None and uuid is not None:
            name = agave.meta.getMetadata(uuid=uuid).get('name')

        cu_data = __to_cu_data(name, value, validate=True)
        if uuid is None:
            resp = agave.meta.addMetadata(body=cu_data)
        else:
            resp = agave.meta.updateMetadata(body=cu_data, uuid=uuid)

        return resp

    except Exception:
        if permissive:
            return {}
        else:
            raise
