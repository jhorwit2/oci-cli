# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import json
import pytest
from tests import generated_test_request_transformers
from tests import test_config_container  # noqa: F401
from tests import util
import vcr
import oci_cli
import os


@pytest.fixture(autouse=True, scope='function')
def vcr_fixture(request):
    # use the default matching logic (link below) with the exception of 'session_agnostic_query_matcher'
    # instead of 'query' matcher (which ignores sessionId in the url)
    # https://vcrpy.readthedocs.io/en/latest/configuration.html#request-matching
    custom_vcr = test_config_container.create_vcr(cassette_library_dir="services/database/tests/cassettes/for_generated")

    cassette_location = 'database_{name}.yml'.format(name=request.function.__name__)
    with custom_vcr.use_cassette(cassette_location):
        yield


@pytest.mark.generated
def test_complete_external_backup_job(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CompleteExternalBackupJob'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CompleteExternalBackupJob')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_complete_external_backup_job.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_complete_external_backup_job', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_complete_external_backup_job.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_complete_external_backup_job'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_complete_external_backup_job.pem'])
            config_file = 'tests/resources/config_for_test_complete_external_backup_job'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('external_backup_job_group.command_name', 'external_backup_job')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CompleteExternalBackupJob')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CompleteExternalBackupJobDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CompleteExternalBackupJob', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('complete_external_backup_job.command_name', 'complete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CompleteExternalBackupJob. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('complete_external_backup_job.command_name', 'complete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('complete_external_backup_job.command_name', 'complete')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CompleteExternalBackupJob',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'externalBackupJob',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_complete_external_backup_job.pem'):
                    os.remove('tests/resources/keyfile_for_test_complete_external_backup_job.pem')
                if os.path.exists('tests/resources/config_for_test_complete_external_backup_job'):
                    os.remove('tests/resources/config_for_test_complete_external_backup_job')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CompleteExternalBackupJob')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_create_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateAutonomousDataWarehouseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_autonomous_data_warehouse.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_data_warehouse.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_data_warehouse.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouse',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_create_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_create_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_autonomous_data_warehouse_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateAutonomousDataWarehouseBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateAutonomousDataWarehouseBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_autonomous_data_warehouse_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_autonomous_data_warehouse_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_autonomous_data_warehouse_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_autonomous_data_warehouse_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_autonomous_data_warehouse_backup.pem'])
            config_file = 'tests/resources/config_for_test_create_autonomous_data_warehouse_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_backup_group.command_name', 'autonomous_data_warehouse_backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDataWarehouseBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateAutonomousDataWarehouseBackupDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateAutonomousDataWarehouseBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_autonomous_data_warehouse_backup.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateAutonomousDataWarehouseBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_data_warehouse_backup.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_data_warehouse_backup.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateAutonomousDataWarehouseBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouseBackup',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_autonomous_data_warehouse_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_autonomous_data_warehouse_backup.pem')
                if os.path.exists('tests/resources/config_for_test_create_autonomous_data_warehouse_backup'):
                    os.remove('tests/resources/config_for_test_create_autonomous_data_warehouse_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDataWarehouseBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_create_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateAutonomousDatabaseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            if request.get('source') == 'DATABASE':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_autonomous_database_create_autonomous_database_clone_details.command_name', 'create-autonomous-database-create-autonomous-database-clone-details')
                )

                if params:
                    del request['source']

            if request.get('source') == 'NONE':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_autonomous_database_create_autonomous_database_details.command_name', 'create-autonomous-database-create-autonomous-database-details')
                )

                if params:
                    del request['source']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_autonomous_database.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_database.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_database.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabase',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_create_autonomous_database'):
                    os.remove('tests/resources/config_for_test_create_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_autonomous_database_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateAutonomousDatabaseBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateAutonomousDatabaseBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_autonomous_database_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_autonomous_database_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_autonomous_database_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_autonomous_database_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_autonomous_database_backup.pem'])
            config_file = 'tests/resources/config_for_test_create_autonomous_database_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_backup_group.command_name', 'autonomous_database_backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDatabaseBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateAutonomousDatabaseBackupDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateAutonomousDatabaseBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_autonomous_database_backup.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateAutonomousDatabaseBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_database_backup.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_autonomous_database_backup.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateAutonomousDatabaseBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabaseBackup',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_autonomous_database_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_autonomous_database_backup.pem')
                if os.path.exists('tests/resources/config_for_test_create_autonomous_database_backup'):
                    os.remove('tests/resources/config_for_test_create_autonomous_database_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateAutonomousDatabaseBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_backup.pem'])
            config_file = 'tests/resources/config_for_test_create_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('backup_group.command_name', 'backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateBackupDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_backup.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_backup.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_backup.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'backup',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_backup.pem')
                if os.path.exists('tests/resources/config_for_test_create_backup'):
                    os.remove('tests/resources/config_for_test_create_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_data_guard_association(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateDataGuardAssociation'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateDataGuardAssociation')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_data_guard_association.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_data_guard_association', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_data_guard_association.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_data_guard_association'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_data_guard_association.pem'])
            config_file = 'tests/resources/config_for_test_create_data_guard_association'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('data_guard_association_group.command_name', 'data_guard_association')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateDataGuardAssociation')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateDataGuardAssociationDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            if request.get('creationType') == 'NewDbSystem':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_data_guard_association_create_data_guard_association_with_new_db_system_details.command_name', 'create-data-guard-association-create-data-guard-association-with-new-db-system-details')
                )

                if params:
                    del request['creationType']

            if request.get('creationType') == 'ExistingDbSystem':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_data_guard_association_create_data_guard_association_to_existing_db_system_details.command_name', 'create-data-guard-association-create-data-guard-association-to-existing-db-system-details')
                )

                if params:
                    del request['creationType']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateDataGuardAssociation', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_data_guard_association.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateDataGuardAssociation. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_data_guard_association.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_data_guard_association.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateDataGuardAssociation',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dataGuardAssociation',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_data_guard_association.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_data_guard_association.pem')
                if os.path.exists('tests/resources/config_for_test_create_data_guard_association'):
                    os.remove('tests/resources/config_for_test_create_data_guard_association')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateDataGuardAssociation')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_db_home(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateDbHome'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateDbHome')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_db_home.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_db_home', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_db_home.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_db_home'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_db_home.pem'])
            config_file = 'tests/resources/config_for_test_create_db_home'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_home_group.command_name', 'db_home')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateDbHome')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateDbHomeWithDbSystemIdDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            if request.get('source') == 'DB_BACKUP':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_db_home_create_db_home_with_db_system_id_from_backup_details.command_name', 'create-db-home-create-db-home-with-db-system-id-from-backup-details')
                )

                if params:
                    del request['source']

            if request.get('source') == 'NONE':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_db_home_create_db_home_with_db_system_id_details.command_name', 'create-db-home-create-db-home-with-db-system-id-details')
                )

                if params:
                    del request['source']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateDbHome', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_db_home.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateDbHome. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_db_home.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_db_home.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateDbHome',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbHome',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_db_home.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_db_home.pem')
                if os.path.exists('tests/resources/config_for_test_create_db_home'):
                    os.remove('tests/resources/config_for_test_create_db_home')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateDbHome')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_external_backup_job(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'CreateExternalBackupJob'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'CreateExternalBackupJob')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_external_backup_job.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_external_backup_job', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_external_backup_job.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_external_backup_job'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_external_backup_job.pem'])
            config_file = 'tests/resources/config_for_test_create_external_backup_job'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('external_backup_job_group.command_name', 'external_backup_job')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateExternalBackupJob')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateExternalBackupJobDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'CreateExternalBackupJob', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_external_backup_job.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, CreateExternalBackupJob. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_external_backup_job.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_external_backup_job.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'CreateExternalBackupJob',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'externalBackupJob',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_external_backup_job.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_external_backup_job.pem')
                if os.path.exists('tests/resources/config_for_test_create_external_backup_job'):
                    os.remove('tests/resources/config_for_test_create_external_backup_job')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='CreateExternalBackupJob')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_db_node_action(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'DbNodeAction'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'DbNodeAction')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_db_node_action.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_db_node_action', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_db_node_action.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_db_node_action'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_db_node_action.pem'])
            config_file = 'tests/resources/config_for_test_db_node_action'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_node_group.command_name', 'db_node')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DbNodeAction')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'DbNodeAction', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('db_node_action.command_name', 'db-node-action')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, DbNodeAction. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('db_node_action.command_name', 'db-node-action'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('db_node_action.command_name', 'db-node-action')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'DbNodeAction',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbNode',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_db_node_action.pem'):
                    os.remove('tests/resources/keyfile_for_test_db_node_action.pem')
                if os.path.exists('tests/resources/config_for_test_db_node_action'):
                    os.remove('tests/resources/config_for_test_db_node_action')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DbNodeAction')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_delete_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'DeleteAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'DeleteAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_delete_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_delete_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_delete_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_delete_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_delete_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_delete_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'DeleteAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('delete_autonomous_data_warehouse.command_name', 'delete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, DeleteAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_autonomous_data_warehouse.command_name', 'delete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_autonomous_data_warehouse.command_name', 'delete')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'DeleteAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'deleteAutonomousDataWarehouse',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_delete_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_delete_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_delete_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_delete_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_delete_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'DeleteAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'DeleteAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_delete_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_delete_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_delete_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_delete_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_delete_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_delete_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'DeleteAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('delete_autonomous_database.command_name', 'delete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, DeleteAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_autonomous_database.command_name', 'delete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_autonomous_database.command_name', 'delete')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'DeleteAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'deleteAutonomousDatabase',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_delete_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_delete_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_delete_autonomous_database'):
                    os.remove('tests/resources/config_for_test_delete_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_delete_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'DeleteBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'DeleteBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_delete_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_delete_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_delete_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_delete_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_delete_backup.pem'])
            config_file = 'tests/resources/config_for_test_delete_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('backup_group.command_name', 'backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'DeleteBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('delete_backup.command_name', 'delete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, DeleteBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_backup.command_name', 'delete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_backup.command_name', 'delete')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'DeleteBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'deleteBackup',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_delete_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_delete_backup.pem')
                if os.path.exists('tests/resources/config_for_test_delete_backup'):
                    os.remove('tests/resources/config_for_test_delete_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_delete_db_home(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'DeleteDbHome'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'DeleteDbHome')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_delete_db_home.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_delete_db_home', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_delete_db_home.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_delete_db_home'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_delete_db_home.pem'])
            config_file = 'tests/resources/config_for_test_delete_db_home'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_home_group.command_name', 'db_home')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteDbHome')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'DeleteDbHome', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('delete_db_home.command_name', 'delete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, DeleteDbHome. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_db_home.command_name', 'delete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_db_home.command_name', 'delete')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'DeleteDbHome',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'deleteDbHome',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_delete_db_home.pem'):
                    os.remove('tests/resources/keyfile_for_test_delete_db_home.pem')
                if os.path.exists('tests/resources/config_for_test_delete_db_home'):
                    os.remove('tests/resources/config_for_test_delete_db_home')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='DeleteDbHome')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_failover_data_guard_association(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'FailoverDataGuardAssociation'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'FailoverDataGuardAssociation')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_failover_data_guard_association.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_failover_data_guard_association', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_failover_data_guard_association.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_failover_data_guard_association'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_failover_data_guard_association.pem'])
            config_file = 'tests/resources/config_for_test_failover_data_guard_association'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('data_guard_association_group.command_name', 'data_guard_association')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='FailoverDataGuardAssociation')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'FailoverDataGuardAssociationDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'FailoverDataGuardAssociation', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('failover_data_guard_association.command_name', 'failover')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, FailoverDataGuardAssociation. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('failover_data_guard_association.command_name', 'failover'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('failover_data_guard_association.command_name', 'failover')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'FailoverDataGuardAssociation',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dataGuardAssociation',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_failover_data_guard_association.pem'):
                    os.remove('tests/resources/keyfile_for_test_failover_data_guard_association.pem')
                if os.path.exists('tests/resources/config_for_test_failover_data_guard_association'):
                    os.remove('tests/resources/config_for_test_failover_data_guard_association')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='FailoverDataGuardAssociation')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_generate_autonomous_data_warehouse_wallet(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GenerateAutonomousDataWarehouseWallet'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GenerateAutonomousDataWarehouseWallet')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_generate_autonomous_data_warehouse_wallet.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_generate_autonomous_data_warehouse_wallet', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_generate_autonomous_data_warehouse_wallet.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_generate_autonomous_data_warehouse_wallet'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_generate_autonomous_data_warehouse_wallet.pem'])
            config_file = 'tests/resources/config_for_test_generate_autonomous_data_warehouse_wallet'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GenerateAutonomousDataWarehouseWallet')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'GenerateAutonomousDataWarehouseWalletDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GenerateAutonomousDataWarehouseWallet', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('generate_autonomous_data_warehouse_wallet.command_name', 'generate-autonomous-data-warehouse-wallet')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GenerateAutonomousDataWarehouseWallet. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('generate_autonomous_data_warehouse_wallet.command_name', 'generate-autonomous-data-warehouse-wallet'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('generate_autonomous_data_warehouse_wallet.command_name', 'generate-autonomous-data-warehouse-wallet')))

            params.extend(['--from-json', input_content])
            import tempfile
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp_file_name = tmp.name
            tmp.close()
            try:
                params.extend(['--file', tmp_file_name])
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GenerateAutonomousDataWarehouseWallet',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'binary',
                    False,
                    True,
                    tmp_file_name
                )
            finally:
                if os.path.isfile(tmp_file_name):
                    os.unlink(tmp_file_name)  # deletes the file
                if os.path.exists('tests/resources/keyfile_for_test_generate_autonomous_data_warehouse_wallet.pem'):
                    os.remove('tests/resources/keyfile_for_test_generate_autonomous_data_warehouse_wallet.pem')
                if os.path.exists('tests/resources/config_for_test_generate_autonomous_data_warehouse_wallet'):
                    os.remove('tests/resources/config_for_test_generate_autonomous_data_warehouse_wallet')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GenerateAutonomousDataWarehouseWallet')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_generate_autonomous_database_wallet(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GenerateAutonomousDatabaseWallet'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GenerateAutonomousDatabaseWallet')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_generate_autonomous_database_wallet.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_generate_autonomous_database_wallet', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_generate_autonomous_database_wallet.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_generate_autonomous_database_wallet'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_generate_autonomous_database_wallet.pem'])
            config_file = 'tests/resources/config_for_test_generate_autonomous_database_wallet'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GenerateAutonomousDatabaseWallet')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'GenerateAutonomousDatabaseWalletDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GenerateAutonomousDatabaseWallet', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('generate_autonomous_database_wallet.command_name', 'generate-autonomous-database-wallet')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GenerateAutonomousDatabaseWallet. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('generate_autonomous_database_wallet.command_name', 'generate-autonomous-database-wallet'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('generate_autonomous_database_wallet.command_name', 'generate-autonomous-database-wallet')))

            params.extend(['--from-json', input_content])
            import tempfile
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp_file_name = tmp.name
            tmp.close()
            try:
                params.extend(['--file', tmp_file_name])
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GenerateAutonomousDatabaseWallet',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'binary',
                    False,
                    True,
                    tmp_file_name
                )
            finally:
                if os.path.isfile(tmp_file_name):
                    os.unlink(tmp_file_name)  # deletes the file
                if os.path.exists('tests/resources/keyfile_for_test_generate_autonomous_database_wallet.pem'):
                    os.remove('tests/resources/keyfile_for_test_generate_autonomous_database_wallet.pem')
                if os.path.exists('tests/resources/config_for_test_generate_autonomous_database_wallet'):
                    os.remove('tests/resources/config_for_test_generate_autonomous_database_wallet')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GenerateAutonomousDatabaseWallet')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_get_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_autonomous_data_warehouse.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_data_warehouse.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_data_warehouse.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouse',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_get_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_get_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_autonomous_data_warehouse_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetAutonomousDataWarehouseBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetAutonomousDataWarehouseBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_autonomous_data_warehouse_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_autonomous_data_warehouse_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_autonomous_data_warehouse_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_autonomous_data_warehouse_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_autonomous_data_warehouse_backup.pem'])
            config_file = 'tests/resources/config_for_test_get_autonomous_data_warehouse_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_backup_group.command_name', 'autonomous_data_warehouse_backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDataWarehouseBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetAutonomousDataWarehouseBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_autonomous_data_warehouse_backup.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetAutonomousDataWarehouseBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_data_warehouse_backup.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_data_warehouse_backup.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetAutonomousDataWarehouseBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouseBackup',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_autonomous_data_warehouse_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_autonomous_data_warehouse_backup.pem')
                if os.path.exists('tests/resources/config_for_test_get_autonomous_data_warehouse_backup'):
                    os.remove('tests/resources/config_for_test_get_autonomous_data_warehouse_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDataWarehouseBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_get_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_autonomous_database.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_database.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_database.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabase',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_get_autonomous_database'):
                    os.remove('tests/resources/config_for_test_get_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_autonomous_database_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetAutonomousDatabaseBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetAutonomousDatabaseBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_autonomous_database_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_autonomous_database_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_autonomous_database_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_autonomous_database_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_autonomous_database_backup.pem'])
            config_file = 'tests/resources/config_for_test_get_autonomous_database_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_backup_group.command_name', 'autonomous_database_backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDatabaseBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetAutonomousDatabaseBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_autonomous_database_backup.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetAutonomousDatabaseBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_database_backup.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_autonomous_database_backup.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetAutonomousDatabaseBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabaseBackup',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_autonomous_database_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_autonomous_database_backup.pem')
                if os.path.exists('tests/resources/config_for_test_get_autonomous_database_backup'):
                    os.remove('tests/resources/config_for_test_get_autonomous_database_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetAutonomousDatabaseBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_backup(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetBackup'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetBackup')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_backup.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_backup', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_backup.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_backup'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_backup.pem'])
            config_file = 'tests/resources/config_for_test_get_backup'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('backup_group.command_name', 'backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetBackup')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetBackup', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_backup.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetBackup. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_backup.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_backup.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetBackup',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'backup',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_backup.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_backup.pem')
                if os.path.exists('tests/resources/config_for_test_get_backup'):
                    os.remove('tests/resources/config_for_test_get_backup')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetBackup')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_data_guard_association(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDataGuardAssociation'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDataGuardAssociation')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_data_guard_association.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_data_guard_association', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_data_guard_association.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_data_guard_association'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_data_guard_association.pem'])
            config_file = 'tests/resources/config_for_test_get_data_guard_association'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('data_guard_association_group.command_name', 'data_guard_association')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDataGuardAssociation')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDataGuardAssociation', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_data_guard_association.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDataGuardAssociation. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_data_guard_association.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_data_guard_association.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDataGuardAssociation',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dataGuardAssociation',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_data_guard_association.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_data_guard_association.pem')
                if os.path.exists('tests/resources/config_for_test_get_data_guard_association'):
                    os.remove('tests/resources/config_for_test_get_data_guard_association')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDataGuardAssociation')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_database.pem'])
            config_file = 'tests/resources/config_for_test_get_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('database_group.command_name', 'database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_database.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_database.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_database.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'database',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_database.pem')
                if os.path.exists('tests/resources/config_for_test_get_database'):
                    os.remove('tests/resources/config_for_test_get_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_home(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbHome'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbHome')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_home.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_home', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_home.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_home'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_home.pem'])
            config_file = 'tests/resources/config_for_test_get_db_home'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_home_group.command_name', 'db_home')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbHome')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbHome', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_home.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbHome. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_home.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_home.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbHome',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbHome',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_home.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_home.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_home'):
                    os.remove('tests/resources/config_for_test_get_db_home')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbHome')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_home_patch(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbHomePatch'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbHomePatch')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_home_patch.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_home_patch', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_home_patch.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_home_patch'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_home_patch.pem'])
            config_file = 'tests/resources/config_for_test_get_db_home_patch'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_group.command_name', 'patch')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbHomePatch')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbHomePatch', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_home_patch.command_name', 'get-db-home')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbHomePatch. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_home_patch.command_name', 'get-db-home'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_home_patch.command_name', 'get-db-home')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbHomePatch',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'patch',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_home_patch.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_home_patch.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_home_patch'):
                    os.remove('tests/resources/config_for_test_get_db_home_patch')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbHomePatch')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_home_patch_history_entry(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbHomePatchHistoryEntry'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbHomePatchHistoryEntry')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_home_patch_history_entry.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_home_patch_history_entry', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_home_patch_history_entry.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_home_patch_history_entry'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_home_patch_history_entry.pem'])
            config_file = 'tests/resources/config_for_test_get_db_home_patch_history_entry'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_history_entry_group.command_name', 'patch_history_entry')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbHomePatchHistoryEntry')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbHomePatchHistoryEntry', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_home_patch_history_entry.command_name', 'get-db-home')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbHomePatchHistoryEntry. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_home_patch_history_entry.command_name', 'get-db-home'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_home_patch_history_entry.command_name', 'get-db-home')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbHomePatchHistoryEntry',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'patchHistoryEntry',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_home_patch_history_entry.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_home_patch_history_entry.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_home_patch_history_entry'):
                    os.remove('tests/resources/config_for_test_get_db_home_patch_history_entry')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbHomePatchHistoryEntry')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_node(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbNode'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbNode')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_node.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_node', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_node.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_node'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_node.pem'])
            config_file = 'tests/resources/config_for_test_get_db_node'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_node_group.command_name', 'db_node')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbNode')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbNode', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_node.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbNode. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_node.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_node.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbNode',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbNode',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_node.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_node.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_node'):
                    os.remove('tests/resources/config_for_test_get_db_node')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbNode')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_system(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbSystem'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbSystem')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_system.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_system', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_system.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_system'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_system.pem'])
            config_file = 'tests/resources/config_for_test_get_db_system'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbSystem')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbSystem', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_system.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbSystem. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_system.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_system.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbSystem',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbSystem',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_system.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_system.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_system'):
                    os.remove('tests/resources/config_for_test_get_db_system')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbSystem')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_system_patch(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbSystemPatch'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbSystemPatch')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_system_patch.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_system_patch', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_system_patch.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_system_patch'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_system_patch.pem'])
            config_file = 'tests/resources/config_for_test_get_db_system_patch'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_group.command_name', 'patch')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbSystemPatch')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbSystemPatch', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_system_patch.command_name', 'get-db-system')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbSystemPatch. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_system_patch.command_name', 'get-db-system'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_system_patch.command_name', 'get-db-system')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbSystemPatch',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'patch',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_system_patch.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_system_patch.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_system_patch'):
                    os.remove('tests/resources/config_for_test_get_db_system_patch')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbSystemPatch')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_db_system_patch_history_entry(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetDbSystemPatchHistoryEntry'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetDbSystemPatchHistoryEntry')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_db_system_patch_history_entry.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_db_system_patch_history_entry', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_db_system_patch_history_entry.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_db_system_patch_history_entry'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_db_system_patch_history_entry.pem'])
            config_file = 'tests/resources/config_for_test_get_db_system_patch_history_entry'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_history_entry_group.command_name', 'patch_history_entry')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbSystemPatchHistoryEntry')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetDbSystemPatchHistoryEntry', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_db_system_patch_history_entry.command_name', 'get-db-system')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetDbSystemPatchHistoryEntry. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_system_patch_history_entry.command_name', 'get-db-system'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_db_system_patch_history_entry.command_name', 'get-db-system')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetDbSystemPatchHistoryEntry',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'patchHistoryEntry',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_db_system_patch_history_entry.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_db_system_patch_history_entry.pem')
                if os.path.exists('tests/resources/config_for_test_get_db_system_patch_history_entry'):
                    os.remove('tests/resources/config_for_test_get_db_system_patch_history_entry')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetDbSystemPatchHistoryEntry')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_exadata_iorm_config(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetExadataIormConfig'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetExadataIormConfig')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_exadata_iorm_config.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_exadata_iorm_config', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_exadata_iorm_config.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_exadata_iorm_config'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_exadata_iorm_config.pem'])
            config_file = 'tests/resources/config_for_test_get_exadata_iorm_config'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetExadataIormConfig')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetExadataIormConfig', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_exadata_iorm_config.command_name', 'get-exadata-iorm-config')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetExadataIormConfig. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_exadata_iorm_config.command_name', 'get-exadata-iorm-config'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_exadata_iorm_config.command_name', 'get-exadata-iorm-config')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetExadataIormConfig',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'exadataIormConfig',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_exadata_iorm_config.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_exadata_iorm_config.pem')
                if os.path.exists('tests/resources/config_for_test_get_exadata_iorm_config'):
                    os.remove('tests/resources/config_for_test_get_exadata_iorm_config')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetExadataIormConfig')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_external_backup_job(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'GetExternalBackupJob'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'GetExternalBackupJob')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_external_backup_job.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_external_backup_job', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_external_backup_job.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_external_backup_job'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_external_backup_job.pem'])
            config_file = 'tests/resources/config_for_test_get_external_backup_job'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('external_backup_job_group.command_name', 'external_backup_job')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetExternalBackupJob')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'GetExternalBackupJob', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_external_backup_job.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, GetExternalBackupJob. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_external_backup_job.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_external_backup_job.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'GetExternalBackupJob',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'externalBackupJob',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_external_backup_job.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_external_backup_job.pem')
                if os.path.exists('tests/resources/config_for_test_get_external_backup_job'):
                    os.remove('tests/resources/config_for_test_get_external_backup_job')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='GetExternalBackupJob')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_launch_db_system(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'LaunchDbSystem'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'LaunchDbSystem')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_launch_db_system.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_launch_db_system', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_launch_db_system.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_launch_db_system'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_launch_db_system.pem'])
            config_file = 'tests/resources/config_for_test_launch_db_system'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='LaunchDbSystem')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'LaunchDbSystemDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            if request.get('source') == 'NONE':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('launch_db_system_launch_db_system_details.command_name', 'launch-db-system-launch-db-system-details')
                )

                if params:
                    del request['source']

            if request.get('source') == 'DB_BACKUP':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('launch_db_system_launch_db_system_from_backup_details.command_name', 'launch-db-system-launch-db-system-from-backup-details')
                )

                if params:
                    del request['source']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'LaunchDbSystem', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('launch_db_system.command_name', 'launch')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, LaunchDbSystem. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('launch_db_system.command_name', 'launch'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('launch_db_system.command_name', 'launch')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'LaunchDbSystem',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbSystem',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_launch_db_system.pem'):
                    os.remove('tests/resources/keyfile_for_test_launch_db_system.pem')
                if os.path.exists('tests/resources/config_for_test_launch_db_system'):
                    os.remove('tests/resources/config_for_test_launch_db_system')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='LaunchDbSystem')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_autonomous_data_warehouse_backups(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListAutonomousDataWarehouseBackups'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListAutonomousDataWarehouseBackups')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_autonomous_data_warehouse_backups.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_autonomous_data_warehouse_backups', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_autonomous_data_warehouse_backups.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_autonomous_data_warehouse_backups'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_autonomous_data_warehouse_backups.pem'])
            config_file = 'tests/resources/config_for_test_list_autonomous_data_warehouse_backups'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_backup_group.command_name', 'autonomous_data_warehouse_backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDataWarehouseBackups')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListAutonomousDataWarehouseBackups', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_autonomous_data_warehouse_backups.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListAutonomousDataWarehouseBackups. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_data_warehouse_backups.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_data_warehouse_backups.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListAutonomousDataWarehouseBackups',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_autonomous_data_warehouse_backups.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_autonomous_data_warehouse_backups.pem')
                if os.path.exists('tests/resources/config_for_test_list_autonomous_data_warehouse_backups'):
                    os.remove('tests/resources/config_for_test_list_autonomous_data_warehouse_backups')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDataWarehouseBackups')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_autonomous_data_warehouses(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListAutonomousDataWarehouses'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListAutonomousDataWarehouses')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_autonomous_data_warehouses.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_autonomous_data_warehouses', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_autonomous_data_warehouses.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_autonomous_data_warehouses'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_autonomous_data_warehouses.pem'])
            config_file = 'tests/resources/config_for_test_list_autonomous_data_warehouses'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDataWarehouses')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListAutonomousDataWarehouses', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_autonomous_data_warehouses.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListAutonomousDataWarehouses. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_data_warehouses.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_data_warehouses.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListAutonomousDataWarehouses',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_autonomous_data_warehouses.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_autonomous_data_warehouses.pem')
                if os.path.exists('tests/resources/config_for_test_list_autonomous_data_warehouses'):
                    os.remove('tests/resources/config_for_test_list_autonomous_data_warehouses')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDataWarehouses')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_autonomous_database_backups(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListAutonomousDatabaseBackups'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListAutonomousDatabaseBackups')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_autonomous_database_backups.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_autonomous_database_backups', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_autonomous_database_backups.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_autonomous_database_backups'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_autonomous_database_backups.pem'])
            config_file = 'tests/resources/config_for_test_list_autonomous_database_backups'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_backup_group.command_name', 'autonomous_database_backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDatabaseBackups')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListAutonomousDatabaseBackups', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_autonomous_database_backups.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListAutonomousDatabaseBackups. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_database_backups.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_database_backups.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListAutonomousDatabaseBackups',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_autonomous_database_backups.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_autonomous_database_backups.pem')
                if os.path.exists('tests/resources/config_for_test_list_autonomous_database_backups'):
                    os.remove('tests/resources/config_for_test_list_autonomous_database_backups')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDatabaseBackups')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_autonomous_databases(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListAutonomousDatabases'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListAutonomousDatabases')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_autonomous_databases.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_autonomous_databases', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_autonomous_databases.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_autonomous_databases'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_autonomous_databases.pem'])
            config_file = 'tests/resources/config_for_test_list_autonomous_databases'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDatabases')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListAutonomousDatabases', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_autonomous_databases.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListAutonomousDatabases. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_databases.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_autonomous_databases.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListAutonomousDatabases',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_autonomous_databases.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_autonomous_databases.pem')
                if os.path.exists('tests/resources/config_for_test_list_autonomous_databases'):
                    os.remove('tests/resources/config_for_test_list_autonomous_databases')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListAutonomousDatabases')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_backups(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListBackups'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListBackups')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_backups.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_backups', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_backups.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_backups'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_backups.pem'])
            config_file = 'tests/resources/config_for_test_list_backups'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('backup_group.command_name', 'backup')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListBackups')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListBackups', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_backups.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListBackups. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_backups.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_backups.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListBackups',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_backups.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_backups.pem')
                if os.path.exists('tests/resources/config_for_test_list_backups'):
                    os.remove('tests/resources/config_for_test_list_backups')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListBackups')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_data_guard_associations(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDataGuardAssociations'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDataGuardAssociations')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_data_guard_associations.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_data_guard_associations', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_data_guard_associations.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_data_guard_associations'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_data_guard_associations.pem'])
            config_file = 'tests/resources/config_for_test_list_data_guard_associations'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('data_guard_association_group.command_name', 'data_guard_association')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDataGuardAssociations')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDataGuardAssociations', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_data_guard_associations.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDataGuardAssociations. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_data_guard_associations.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_data_guard_associations.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDataGuardAssociations',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_data_guard_associations.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_data_guard_associations.pem')
                if os.path.exists('tests/resources/config_for_test_list_data_guard_associations'):
                    os.remove('tests/resources/config_for_test_list_data_guard_associations')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDataGuardAssociations')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_databases(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDatabases'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDatabases')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_databases.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_databases', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_databases.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_databases'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_databases.pem'])
            config_file = 'tests/resources/config_for_test_list_databases'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('database_group.command_name', 'database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDatabases')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDatabases', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_databases.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDatabases. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_databases.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_databases.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDatabases',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_databases.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_databases.pem')
                if os.path.exists('tests/resources/config_for_test_list_databases'):
                    os.remove('tests/resources/config_for_test_list_databases')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDatabases')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_home_patch_history_entries(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbHomePatchHistoryEntries'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbHomePatchHistoryEntries')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_home_patch_history_entries.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_home_patch_history_entries', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_home_patch_history_entries.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_home_patch_history_entries'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_home_patch_history_entries.pem'])
            config_file = 'tests/resources/config_for_test_list_db_home_patch_history_entries'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_history_entry_group.command_name', 'patch_history_entry')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbHomePatchHistoryEntries')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbHomePatchHistoryEntries', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_home_patch_history_entries.command_name', 'list-db-home')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbHomePatchHistoryEntries. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_home_patch_history_entries.command_name', 'list-db-home'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_home_patch_history_entries.command_name', 'list-db-home')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbHomePatchHistoryEntries',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_home_patch_history_entries.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_home_patch_history_entries.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_home_patch_history_entries'):
                    os.remove('tests/resources/config_for_test_list_db_home_patch_history_entries')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbHomePatchHistoryEntries')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_home_patches(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbHomePatches'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbHomePatches')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_home_patches.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_home_patches', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_home_patches.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_home_patches'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_home_patches.pem'])
            config_file = 'tests/resources/config_for_test_list_db_home_patches'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_group.command_name', 'patch')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbHomePatches')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbHomePatches', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_home_patches.command_name', 'list-db-home')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbHomePatches. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_home_patches.command_name', 'list-db-home'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_home_patches.command_name', 'list-db-home')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbHomePatches',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_home_patches.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_home_patches.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_home_patches'):
                    os.remove('tests/resources/config_for_test_list_db_home_patches')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbHomePatches')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_homes(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbHomes'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbHomes')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_homes.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_homes', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_homes.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_homes'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_homes.pem'])
            config_file = 'tests/resources/config_for_test_list_db_homes'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_home_group.command_name', 'db_home')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbHomes')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbHomes', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_homes.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbHomes. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_homes.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_homes.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbHomes',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_homes.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_homes.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_homes'):
                    os.remove('tests/resources/config_for_test_list_db_homes')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbHomes')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_nodes(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbNodes'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbNodes')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_nodes.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_nodes', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_nodes.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_nodes'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_nodes.pem'])
            config_file = 'tests/resources/config_for_test_list_db_nodes'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_node_group.command_name', 'db_node')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbNodes')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbNodes', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_nodes.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbNodes. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_nodes.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_nodes.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbNodes',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_nodes.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_nodes.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_nodes'):
                    os.remove('tests/resources/config_for_test_list_db_nodes')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbNodes')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_system_patch_history_entries(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbSystemPatchHistoryEntries'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbSystemPatchHistoryEntries')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_system_patch_history_entries.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_system_patch_history_entries', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_system_patch_history_entries.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_system_patch_history_entries'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_system_patch_history_entries.pem'])
            config_file = 'tests/resources/config_for_test_list_db_system_patch_history_entries'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_history_entry_group.command_name', 'patch_history_entry')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystemPatchHistoryEntries')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbSystemPatchHistoryEntries', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_system_patch_history_entries.command_name', 'list-db-system')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbSystemPatchHistoryEntries. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_system_patch_history_entries.command_name', 'list-db-system'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_system_patch_history_entries.command_name', 'list-db-system')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbSystemPatchHistoryEntries',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_system_patch_history_entries.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_system_patch_history_entries.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_system_patch_history_entries'):
                    os.remove('tests/resources/config_for_test_list_db_system_patch_history_entries')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystemPatchHistoryEntries')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_system_patches(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbSystemPatches'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbSystemPatches')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_system_patches.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_system_patches', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_system_patches.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_system_patches'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_system_patches.pem'])
            config_file = 'tests/resources/config_for_test_list_db_system_patches'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('patch_group.command_name', 'patch')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystemPatches')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbSystemPatches', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_system_patches.command_name', 'list-db-system')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbSystemPatches. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_system_patches.command_name', 'list-db-system'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_system_patches.command_name', 'list-db-system')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbSystemPatches',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_system_patches.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_system_patches.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_system_patches'):
                    os.remove('tests/resources/config_for_test_list_db_system_patches')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystemPatches')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_system_shapes(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbSystemShapes'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbSystemShapes')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_system_shapes.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_system_shapes', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_system_shapes.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_system_shapes'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_system_shapes.pem'])
            config_file = 'tests/resources/config_for_test_list_db_system_shapes'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_shape_group.command_name', 'db_system_shape')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystemShapes')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbSystemShapes', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_system_shapes.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbSystemShapes. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_system_shapes.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_system_shapes.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbSystemShapes',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_system_shapes.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_system_shapes.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_system_shapes'):
                    os.remove('tests/resources/config_for_test_list_db_system_shapes')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystemShapes')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_systems(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbSystems'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbSystems')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_systems.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_systems', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_systems.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_systems'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_systems.pem'])
            config_file = 'tests/resources/config_for_test_list_db_systems'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystems')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbSystems', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_systems.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbSystems. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_systems.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_systems.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbSystems',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_systems.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_systems.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_systems'):
                    os.remove('tests/resources/config_for_test_list_db_systems')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbSystems')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_db_versions(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ListDbVersions'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ListDbVersions')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_db_versions.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_db_versions', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_db_versions.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_db_versions'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_db_versions.pem'])
            config_file = 'tests/resources/config_for_test_list_db_versions'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_version_group.command_name', 'db_version')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbVersions')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ListDbVersions', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_db_versions.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ListDbVersions. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_versions.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_db_versions.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ListDbVersions',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_db_versions.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_db_versions.pem')
                if os.path.exists('tests/resources/config_for_test_list_db_versions'):
                    os.remove('tests/resources/config_for_test_list_db_versions')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ListDbVersions')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_reinstate_data_guard_association(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'ReinstateDataGuardAssociation'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'ReinstateDataGuardAssociation')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_reinstate_data_guard_association.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_reinstate_data_guard_association', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_reinstate_data_guard_association.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_reinstate_data_guard_association'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_reinstate_data_guard_association.pem'])
            config_file = 'tests/resources/config_for_test_reinstate_data_guard_association'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('data_guard_association_group.command_name', 'data_guard_association')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ReinstateDataGuardAssociation')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'ReinstateDataGuardAssociationDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'ReinstateDataGuardAssociation', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('reinstate_data_guard_association.command_name', 'reinstate')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, ReinstateDataGuardAssociation. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('reinstate_data_guard_association.command_name', 'reinstate'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('reinstate_data_guard_association.command_name', 'reinstate')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'ReinstateDataGuardAssociation',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dataGuardAssociation',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_reinstate_data_guard_association.pem'):
                    os.remove('tests/resources/keyfile_for_test_reinstate_data_guard_association.pem')
                if os.path.exists('tests/resources/config_for_test_reinstate_data_guard_association'):
                    os.remove('tests/resources/config_for_test_reinstate_data_guard_association')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='ReinstateDataGuardAssociation')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_restore_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'RestoreAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'RestoreAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_restore_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_restore_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_restore_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_restore_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_restore_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_restore_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='RestoreAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'RestoreAutonomousDataWarehouseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'RestoreAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('restore_autonomous_data_warehouse.command_name', 'restore')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, RestoreAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('restore_autonomous_data_warehouse.command_name', 'restore'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('restore_autonomous_data_warehouse.command_name', 'restore')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'RestoreAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouse',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_restore_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_restore_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_restore_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_restore_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='RestoreAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_restore_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'RestoreAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'RestoreAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_restore_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_restore_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_restore_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_restore_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_restore_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_restore_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='RestoreAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'RestoreAutonomousDatabaseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'RestoreAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('restore_autonomous_database.command_name', 'restore')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, RestoreAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('restore_autonomous_database.command_name', 'restore'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('restore_autonomous_database.command_name', 'restore')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'RestoreAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabase',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_restore_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_restore_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_restore_autonomous_database'):
                    os.remove('tests/resources/config_for_test_restore_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='RestoreAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_restore_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'RestoreDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'RestoreDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_restore_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_restore_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_restore_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_restore_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_restore_database.pem'])
            config_file = 'tests/resources/config_for_test_restore_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('database_group.command_name', 'database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='RestoreDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'RestoreDatabaseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'RestoreDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('restore_database.command_name', 'restore')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, RestoreDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('restore_database.command_name', 'restore'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('restore_database.command_name', 'restore')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'RestoreDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'database',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_restore_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_restore_database.pem')
                if os.path.exists('tests/resources/config_for_test_restore_database'):
                    os.remove('tests/resources/config_for_test_restore_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='RestoreDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_start_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'StartAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'StartAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_start_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_start_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_start_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_start_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_start_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_start_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StartAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'StartAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('start_autonomous_data_warehouse.command_name', 'start')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, StartAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('start_autonomous_data_warehouse.command_name', 'start'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('start_autonomous_data_warehouse.command_name', 'start')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'StartAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouse',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_start_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_start_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_start_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_start_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StartAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_start_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'StartAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'StartAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_start_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_start_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_start_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_start_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_start_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_start_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StartAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'StartAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('start_autonomous_database.command_name', 'start')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, StartAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('start_autonomous_database.command_name', 'start'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('start_autonomous_database.command_name', 'start')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'StartAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabase',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_start_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_start_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_start_autonomous_database'):
                    os.remove('tests/resources/config_for_test_start_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StartAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_stop_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'StopAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'StopAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_stop_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_stop_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_stop_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_stop_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_stop_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_stop_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StopAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'StopAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('stop_autonomous_data_warehouse.command_name', 'stop')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, StopAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('stop_autonomous_data_warehouse.command_name', 'stop'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('stop_autonomous_data_warehouse.command_name', 'stop')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'StopAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouse',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_stop_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_stop_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_stop_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_stop_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StopAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_stop_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'StopAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'StopAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_stop_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_stop_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_stop_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_stop_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_stop_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_stop_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StopAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'StopAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('stop_autonomous_database.command_name', 'stop')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, StopAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('stop_autonomous_database.command_name', 'stop'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('stop_autonomous_database.command_name', 'stop')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'StopAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabase',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_stop_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_stop_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_stop_autonomous_database'):
                    os.remove('tests/resources/config_for_test_stop_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='StopAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_switchover_data_guard_association(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'SwitchoverDataGuardAssociation'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'SwitchoverDataGuardAssociation')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_switchover_data_guard_association.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_switchover_data_guard_association', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_switchover_data_guard_association.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_switchover_data_guard_association'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_switchover_data_guard_association.pem'])
            config_file = 'tests/resources/config_for_test_switchover_data_guard_association'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('data_guard_association_group.command_name', 'data_guard_association')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='SwitchoverDataGuardAssociation')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'SwitchoverDataGuardAssociationDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'SwitchoverDataGuardAssociation', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('switchover_data_guard_association.command_name', 'switchover')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, SwitchoverDataGuardAssociation. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('switchover_data_guard_association.command_name', 'switchover'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('switchover_data_guard_association.command_name', 'switchover')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'SwitchoverDataGuardAssociation',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dataGuardAssociation',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_switchover_data_guard_association.pem'):
                    os.remove('tests/resources/keyfile_for_test_switchover_data_guard_association.pem')
                if os.path.exists('tests/resources/config_for_test_switchover_data_guard_association'):
                    os.remove('tests/resources/config_for_test_switchover_data_guard_association')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='SwitchoverDataGuardAssociation')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_terminate_db_system(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'TerminateDbSystem'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'TerminateDbSystem')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_terminate_db_system.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_terminate_db_system', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_terminate_db_system.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_terminate_db_system'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_terminate_db_system.pem'])
            config_file = 'tests/resources/config_for_test_terminate_db_system'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='TerminateDbSystem')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'TerminateDbSystem', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('terminate_db_system.command_name', 'terminate')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, TerminateDbSystem. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('terminate_db_system.command_name', 'terminate'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('terminate_db_system.command_name', 'terminate')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'TerminateDbSystem',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'terminateDbSystem',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_terminate_db_system.pem'):
                    os.remove('tests/resources/keyfile_for_test_terminate_db_system.pem')
                if os.path.exists('tests/resources/config_for_test_terminate_db_system'):
                    os.remove('tests/resources/config_for_test_terminate_db_system')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='TerminateDbSystem')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_autonomous_data_warehouse(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'UpdateAutonomousDataWarehouse'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'UpdateAutonomousDataWarehouse')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_autonomous_data_warehouse.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_autonomous_data_warehouse', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_autonomous_data_warehouse.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_autonomous_data_warehouse'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_autonomous_data_warehouse.pem'])
            config_file = 'tests/resources/config_for_test_update_autonomous_data_warehouse'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_data_warehouse_group.command_name', 'autonomous_data_warehouse')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateAutonomousDataWarehouse')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateAutonomousDataWarehouseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'UpdateAutonomousDataWarehouse', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_autonomous_data_warehouse.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, UpdateAutonomousDataWarehouse. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_autonomous_data_warehouse.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_autonomous_data_warehouse.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'UpdateAutonomousDataWarehouse',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDataWarehouse',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_autonomous_data_warehouse.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_autonomous_data_warehouse.pem')
                if os.path.exists('tests/resources/config_for_test_update_autonomous_data_warehouse'):
                    os.remove('tests/resources/config_for_test_update_autonomous_data_warehouse')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateAutonomousDataWarehouse')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_autonomous_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'UpdateAutonomousDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'UpdateAutonomousDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_autonomous_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_autonomous_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_autonomous_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_autonomous_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_autonomous_database.pem'])
            config_file = 'tests/resources/config_for_test_update_autonomous_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('autonomous_database_group.command_name', 'autonomous_database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateAutonomousDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateAutonomousDatabaseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'UpdateAutonomousDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_autonomous_database.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, UpdateAutonomousDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_autonomous_database.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_autonomous_database.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'UpdateAutonomousDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autonomousDatabase',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_autonomous_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_autonomous_database.pem')
                if os.path.exists('tests/resources/config_for_test_update_autonomous_database'):
                    os.remove('tests/resources/config_for_test_update_autonomous_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateAutonomousDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_database(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'UpdateDatabase'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'UpdateDatabase')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_database.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_database', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_database.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_database'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_database.pem'])
            config_file = 'tests/resources/config_for_test_update_database'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('database_group.command_name', 'database')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateDatabase')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateDatabaseDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'UpdateDatabase', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_database.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, UpdateDatabase. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_database.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_database.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'UpdateDatabase',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'database',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_database.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_database.pem')
                if os.path.exists('tests/resources/config_for_test_update_database'):
                    os.remove('tests/resources/config_for_test_update_database')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateDatabase')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_db_home(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'UpdateDbHome'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'UpdateDbHome')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_db_home.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_db_home', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_db_home.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_db_home'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_db_home.pem'])
            config_file = 'tests/resources/config_for_test_update_db_home'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_home_group.command_name', 'db_home')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateDbHome')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateDbHomeDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'UpdateDbHome', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_db_home.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, UpdateDbHome. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_db_home.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_db_home.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'UpdateDbHome',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbHome',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_db_home.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_db_home.pem')
                if os.path.exists('tests/resources/config_for_test_update_db_home'):
                    os.remove('tests/resources/config_for_test_update_db_home')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateDbHome')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_db_system(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'UpdateDbSystem'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'UpdateDbSystem')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_db_system.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_db_system', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_db_system.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_db_system'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_db_system.pem'])
            config_file = 'tests/resources/config_for_test_update_db_system'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateDbSystem')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateDbSystemDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'UpdateDbSystem', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_db_system.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, UpdateDbSystem. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_db_system.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_db_system.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'UpdateDbSystem',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'dbSystem',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_db_system.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_db_system.pem')
                if os.path.exists('tests/resources/config_for_test_update_db_system'):
                    os.remove('tests/resources/config_for_test_update_db_system')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateDbSystem')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_exadata_iorm_config(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('database', 'UpdateExadataIormConfig'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('database', 'Database', 'UpdateExadataIormConfig')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_exadata_iorm_config.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_exadata_iorm_config', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_exadata_iorm_config.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_exadata_iorm_config'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_exadata_iorm_config.pem'])
            config_file = 'tests/resources/config_for_test_update_exadata_iorm_config'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('db_root_group.command_name', 'db')
    resource_group_command_name = oci_cli.cli_util.override('db_system_group.command_name', 'db_system')
    request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateExadataIormConfig')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'ExadataIormConfigUpdateDetails'
            details = request.pop(param_name[0].lower() + param_name[1:])
            for key in details:
                request[key] = details[key]
                override = util.variable_name_override(key)
                if override:
                    request[override] = request.pop(key)

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('database', 'UpdateExadataIormConfig', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_exadata_iorm_config.command_name', 'update-exadata-iorm-config')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: database, UpdateExadataIormConfig. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_exadata_iorm_config.command_name', 'update-exadata-iorm-config'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_exadata_iorm_config.command_name', 'update-exadata-iorm-config')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'database',
                    'UpdateExadataIormConfig',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'exadataIormConfig',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_exadata_iorm_config.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_exadata_iorm_config.pem')
                if os.path.exists('tests/resources/config_for_test_update_exadata_iorm_config'):
                    os.remove('tests/resources/config_for_test_update_exadata_iorm_config')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='database', api_name='UpdateExadataIormConfig')
                request = request_containers[i]['request'].copy()


def invoke(runner, config_file, config_profile, params, debug=False, root_params=None, strip_progress_bar=True, strip_multipart_stderr_output=True, ** args):
    root_params = ['--config-file', config_file]

    if config_profile:
        root_params.extend(['--profile', config_profile])

    if debug is True:
        result = runner.invoke(oci_cli.cli, root_params + ['--debug'] + params, ** args)
    else:
        result = runner.invoke(oci_cli.cli, root_params + params, ** args)

    return result
