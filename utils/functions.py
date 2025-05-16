import tomli, tomli_w

def modifyConfig(path, keys_values, append=False, verbose=False):
    """Modifies the specified keys in the TOML config file.
    If the key does not exist, it will be created as long as append is True."""

    if not isinstance(keys_values, dict):
        raise TypeError("keys_values must be a dictionary. Like {'key': 'value'}")
    try:
        with open(path, "rb") as file:
            data = tomli.load(file)
        
        for key, value in keys_values.items():
            if key not in data and not append:
                print(f"Key '{key}' not found in the config.")
                raise Exception(f"Key '{key}' not found.")
            if verbose:
                print(f"Setting '{key}' to '{value}'")
            data[key] = value
        
        with open(path, "wb") as file:
            tomli_w.dump(data, file)

        return True    
    except FileNotFoundError:
        print("Config file not found.")
    except (tomli.TOMLDecodeError):
        print("Error reading or writing the config file.")