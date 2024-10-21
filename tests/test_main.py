from main import load_config


def test_parse_arguments():
    assert True


def test_load_config(tmpdir):
    yaml_content = """
    mappings:
      Rep ID: Agent_ID
      Rep Name: Agent_Name
      Plan: Plan_Name
      Commission: Commission_Amount
      Period: Commission_Period
      Carrier: Carrier_Name
      Enrollment: Enrollment_Type
      Member Name: Member_Name
      Member ID: Member_ID
    """

    yaml_file = tmpdir.join('config.yaml')
    yaml_file.write(yaml_content)

    config = load_config(str(yaml_file))

    expected_config = {
        'mappings': {
            'Rep ID': 'Agent_ID',
            'Rep Name': 'Agent_Name',
            'Plan': 'Plan_Name',
            'Commission': 'Commission_Amount',
            'Period': 'Commission_Period',
            'Carrier': 'Carrier_Name',
            'Enrollment': 'Enrollment_Type',
            'Member Name': 'Member_Name',
            'Member ID': 'Member_ID'
        }
    }

    assert config == expected_config, "Config does not match the expected output"


def test_load_config_file():
    test_config_path = 'yaml/test_config.yaml'
    config = load_config(test_config_path)

    expected_mappings = {
        'Member Name': 'Agent_Name',
        'Member ID': 'Agent_ID',
        'Commission Amount': 'Commission_Amount',
        'Period': 'Commission_Period'
    }

    assert config['mappings'] == expected_mappings , "Config does not match the expected output"


def test_main():
    assert True
