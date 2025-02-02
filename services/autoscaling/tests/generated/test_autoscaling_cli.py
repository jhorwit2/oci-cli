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
    custom_vcr = test_config_container.create_vcr(cassette_library_dir="services/autoscaling/tests/cassettes/for_generated")

    cassette_location = 'autoscaling_{name}.yml'.format(name=request.function.__name__)
    with custom_vcr.use_cassette(cassette_location):
        yield


@pytest.mark.generated
def test_create_auto_scaling_configuration(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'CreateAutoScalingConfiguration'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'CreateAutoScalingConfiguration')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_auto_scaling_configuration.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_auto_scaling_configuration', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_auto_scaling_configuration.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_auto_scaling_configuration'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_auto_scaling_configuration.pem'])
            config_file = 'tests/resources/config_for_test_create_auto_scaling_configuration'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_configuration_group.command_name', 'auto_scaling_configuration')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='CreateAutoScalingConfiguration')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateAutoScalingConfigurationDetails'
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

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'CreateAutoScalingConfiguration', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_auto_scaling_configuration.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, CreateAutoScalingConfiguration. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_auto_scaling_configuration.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_auto_scaling_configuration.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'CreateAutoScalingConfiguration',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autoScalingConfiguration',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_auto_scaling_configuration.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_auto_scaling_configuration.pem')
                if os.path.exists('tests/resources/config_for_test_create_auto_scaling_configuration'):
                    os.remove('tests/resources/config_for_test_create_auto_scaling_configuration')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='CreateAutoScalingConfiguration')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_create_auto_scaling_policy(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'CreateAutoScalingPolicy'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'CreateAutoScalingPolicy')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_create_auto_scaling_policy.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_create_auto_scaling_policy', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_create_auto_scaling_policy.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_create_auto_scaling_policy'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_create_auto_scaling_policy.pem'])
            config_file = 'tests/resources/config_for_test_create_auto_scaling_policy'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_policy_group.command_name', 'auto_scaling_policy')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='CreateAutoScalingPolicy')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'CreateAutoScalingPolicyDetails'
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

            if request.get('policyType') == 'threshold':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_auto_scaling_policy_create_threshold_policy_details.command_name', 'create-auto-scaling-policy-create-threshold-policy-details')
                )

                if params:
                    del request['policyType']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'CreateAutoScalingPolicy', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('create_auto_scaling_policy.command_name', 'create')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, CreateAutoScalingPolicy. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_auto_scaling_policy.command_name', 'create'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('create_auto_scaling_policy.command_name', 'create')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'CreateAutoScalingPolicy',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autoScalingPolicy',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_create_auto_scaling_policy.pem'):
                    os.remove('tests/resources/keyfile_for_test_create_auto_scaling_policy.pem')
                if os.path.exists('tests/resources/config_for_test_create_auto_scaling_policy'):
                    os.remove('tests/resources/config_for_test_create_auto_scaling_policy')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='CreateAutoScalingPolicy')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_delete_auto_scaling_configuration(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'DeleteAutoScalingConfiguration'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'DeleteAutoScalingConfiguration')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_delete_auto_scaling_configuration.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_delete_auto_scaling_configuration', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_delete_auto_scaling_configuration.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_delete_auto_scaling_configuration'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_delete_auto_scaling_configuration.pem'])
            config_file = 'tests/resources/config_for_test_delete_auto_scaling_configuration'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_configuration_group.command_name', 'auto_scaling_configuration')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='DeleteAutoScalingConfiguration')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'DeleteAutoScalingConfiguration', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('delete_auto_scaling_configuration.command_name', 'delete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, DeleteAutoScalingConfiguration. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_auto_scaling_configuration.command_name', 'delete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_auto_scaling_configuration.command_name', 'delete')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'DeleteAutoScalingConfiguration',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'deleteAutoScalingConfiguration',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_delete_auto_scaling_configuration.pem'):
                    os.remove('tests/resources/keyfile_for_test_delete_auto_scaling_configuration.pem')
                if os.path.exists('tests/resources/config_for_test_delete_auto_scaling_configuration'):
                    os.remove('tests/resources/config_for_test_delete_auto_scaling_configuration')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='DeleteAutoScalingConfiguration')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_delete_auto_scaling_policy(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'DeleteAutoScalingPolicy'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'DeleteAutoScalingPolicy')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_delete_auto_scaling_policy.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_delete_auto_scaling_policy', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_delete_auto_scaling_policy.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_delete_auto_scaling_policy'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_delete_auto_scaling_policy.pem'])
            config_file = 'tests/resources/config_for_test_delete_auto_scaling_policy'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_policy_group.command_name', 'auto_scaling_policy')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='DeleteAutoScalingPolicy')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'DeleteAutoScalingPolicy', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('delete_auto_scaling_policy.command_name', 'delete')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, DeleteAutoScalingPolicy. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_auto_scaling_policy.command_name', 'delete'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('delete_auto_scaling_policy.command_name', 'delete')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'DeleteAutoScalingPolicy',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'deleteAutoScalingPolicy',
                    True
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_delete_auto_scaling_policy.pem'):
                    os.remove('tests/resources/keyfile_for_test_delete_auto_scaling_policy.pem')
                if os.path.exists('tests/resources/config_for_test_delete_auto_scaling_policy'):
                    os.remove('tests/resources/config_for_test_delete_auto_scaling_policy')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='DeleteAutoScalingPolicy')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_auto_scaling_configuration(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'GetAutoScalingConfiguration'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'GetAutoScalingConfiguration')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_auto_scaling_configuration.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_auto_scaling_configuration', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_auto_scaling_configuration.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_auto_scaling_configuration'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_auto_scaling_configuration.pem'])
            config_file = 'tests/resources/config_for_test_get_auto_scaling_configuration'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_configuration_group.command_name', 'auto_scaling_configuration')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='GetAutoScalingConfiguration')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'GetAutoScalingConfiguration', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_auto_scaling_configuration.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, GetAutoScalingConfiguration. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_auto_scaling_configuration.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_auto_scaling_configuration.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'GetAutoScalingConfiguration',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autoScalingConfiguration',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_auto_scaling_configuration.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_auto_scaling_configuration.pem')
                if os.path.exists('tests/resources/config_for_test_get_auto_scaling_configuration'):
                    os.remove('tests/resources/config_for_test_get_auto_scaling_configuration')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='GetAutoScalingConfiguration')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_get_auto_scaling_policy(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'GetAutoScalingPolicy'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'GetAutoScalingPolicy')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_get_auto_scaling_policy.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_get_auto_scaling_policy', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_get_auto_scaling_policy.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_get_auto_scaling_policy'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_get_auto_scaling_policy.pem'])
            config_file = 'tests/resources/config_for_test_get_auto_scaling_policy'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_policy_group.command_name', 'auto_scaling_policy')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='GetAutoScalingPolicy')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'GetAutoScalingPolicy', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('get_auto_scaling_policy.command_name', 'get')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, GetAutoScalingPolicy. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_auto_scaling_policy.command_name', 'get'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('get_auto_scaling_policy.command_name', 'get')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'GetAutoScalingPolicy',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autoScalingPolicy',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_get_auto_scaling_policy.pem'):
                    os.remove('tests/resources/keyfile_for_test_get_auto_scaling_policy.pem')
                if os.path.exists('tests/resources/config_for_test_get_auto_scaling_policy'):
                    os.remove('tests/resources/config_for_test_get_auto_scaling_policy')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='GetAutoScalingPolicy')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_auto_scaling_configurations(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'ListAutoScalingConfigurations'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'ListAutoScalingConfigurations')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_auto_scaling_configurations.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_auto_scaling_configurations', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_auto_scaling_configurations.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_auto_scaling_configurations'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_auto_scaling_configurations.pem'])
            config_file = 'tests/resources/config_for_test_list_auto_scaling_configurations'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_configuration_group.command_name', 'auto_scaling_configuration')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='ListAutoScalingConfigurations')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'ListAutoScalingConfigurations', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_auto_scaling_configurations.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, ListAutoScalingConfigurations. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_auto_scaling_configurations.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_auto_scaling_configurations.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'ListAutoScalingConfigurations',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_auto_scaling_configurations.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_auto_scaling_configurations.pem')
                if os.path.exists('tests/resources/config_for_test_list_auto_scaling_configurations'):
                    os.remove('tests/resources/config_for_test_list_auto_scaling_configurations')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='ListAutoScalingConfigurations')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_list_auto_scaling_policies(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'ListAutoScalingPolicies'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'ListAutoScalingPolicies')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_list_auto_scaling_policies.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_list_auto_scaling_policies', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_list_auto_scaling_policies.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_list_auto_scaling_policies'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_list_auto_scaling_policies.pem'])
            config_file = 'tests/resources/config_for_test_list_auto_scaling_policies'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_policy_group.command_name', 'auto_scaling_policy')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='ListAutoScalingPolicies')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:

            if 'opts' in request:
                for key in request['opts']:
                    request[key] = request['opts'][key]
                del request['opts']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'ListAutoScalingPolicies', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('list_auto_scaling_policies.command_name', 'list')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, ListAutoScalingPolicies. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_auto_scaling_policies.command_name', 'list'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('list_auto_scaling_policies.command_name', 'list')))

            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'ListAutoScalingPolicies',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'items',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_list_auto_scaling_policies.pem'):
                    os.remove('tests/resources/keyfile_for_test_list_auto_scaling_policies.pem')
                if os.path.exists('tests/resources/config_for_test_list_auto_scaling_policies'):
                    os.remove('tests/resources/config_for_test_list_auto_scaling_policies')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='ListAutoScalingPolicies')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_auto_scaling_configuration(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'UpdateAutoScalingConfiguration'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'UpdateAutoScalingConfiguration')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_auto_scaling_configuration.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_auto_scaling_configuration', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_auto_scaling_configuration.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_auto_scaling_configuration'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_auto_scaling_configuration.pem'])
            config_file = 'tests/resources/config_for_test_update_auto_scaling_configuration'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_configuration_group.command_name', 'auto_scaling_configuration')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='UpdateAutoScalingConfiguration')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateAutoScalingConfigurationDetails'
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

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'UpdateAutoScalingConfiguration', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_auto_scaling_configuration.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, UpdateAutoScalingConfiguration. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_auto_scaling_configuration.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_auto_scaling_configuration.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'UpdateAutoScalingConfiguration',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autoScalingConfiguration',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_auto_scaling_configuration.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_auto_scaling_configuration.pem')
                if os.path.exists('tests/resources/config_for_test_update_auto_scaling_configuration'):
                    os.remove('tests/resources/config_for_test_update_auto_scaling_configuration')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='UpdateAutoScalingConfiguration')
                request = request_containers[i]['request'].copy()


@pytest.mark.generated
def test_update_auto_scaling_policy(cli_testing_service_client, runner, config_file, config_profile):
    if not cli_testing_service_client.is_api_enabled('autoscaling', 'UpdateAutoScalingPolicy'):
        pytest.skip('OCI Testing Service has not been configured for this operation yet.')

    config_file = os.environ['OCI_CLI_CONFIG_FILE']
    if 'USE_TESTING_SERVICE_CONFIG' in os.environ:
        try:
            config_str = cli_testing_service_client.get_config('autoscaling', 'AutoScaling', 'UpdateAutoScalingPolicy')
            config = json.loads(config_str)
            key_file_content = config['keyFileContent']
            with open('tests/resources/keyfile_for_test_update_auto_scaling_policy.pem', 'w') as f:
                f.write(key_file_content)
            with open('tests/resources/config_for_test_update_auto_scaling_policy', 'w') as f:
                f.write('[ADMIN]\n')
                f.write('user = ' + config['userId'] + '\n')
                f.write('fingerprint = ' + config['fingerprint'] + '\n')
                f.write('tenancy = ' + config['tenantId'] + '\n')
                f.write('region = ' + config['region'] + '\n')
                f.write('key_file = tests/resources/keyfile_for_test_update_auto_scaling_policy.pem\n')
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/config_for_test_update_auto_scaling_policy'])
            runner.invoke(oci_cli.cli, ['setup', 'repair-file-permissions', '--file', 'tests/resources/keyfile_for_test_update_auto_scaling_policy.pem'])
            config_file = 'tests/resources/config_for_test_update_auto_scaling_policy'
        except vcr.errors.CannotOverwriteExistingCassetteException:
            pass
        except Exception as e:
            print(e)
            raise e

    root_command_name = oci_cli.cli_util.override('autoscaling_root_group.command_name', 'autoscaling')
    resource_group_command_name = oci_cli.cli_util.override('auto_scaling_policy_group.command_name', 'auto_scaling_policy')
    request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='UpdateAutoScalingPolicy')
    for i in range(len(request_containers)):
        request = request_containers[i]['request'].copy()
        done = False
        params = []
        while not done:
            # force all details param names to have lower case first letter for consistency with Java models
            param_name = 'UpdateAutoScalingPolicyDetails'
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

            if request.get('policyType') == 'threshold':
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_auto_scaling_policy_update_threshold_policy_details.command_name', 'update-auto-scaling-policy-update-threshold-policy-details')
                )

                if params:
                    del request['policyType']

            request, cleanup = generated_test_request_transformers.transform_generated_test_input('autoscaling', 'UpdateAutoScalingPolicy', request)

            input_content = json.dumps(request)

            # for operations with polymorphic input types, attempt to find an operation for a specific subtype
            # if one does not exist, fallback to calling base operation
            if not params:
                params = util.get_command_list(
                    root_command_name,
                    resource_group_command_name,
                    oci_cli.cli_util.override('update_auto_scaling_policy.command_name', 'update')
                )

            if not params:
                raise ValueError(
                    'Failed to find CLI command "oci {} {} {}" for given operation: autoscaling, UpdateAutoScalingPolicy. '
                    'This usually happens because generated commands have been manually re-arranged in code for better user '
                    'experience. To allow this test to find the proper command, please add an entry to MOVED_COMMANDS in '
                    'services/<spec_name>/tests/extend_test_<your_service_name>.py to map ({}, {}, {}) to the syntax '
                    'for the new command. If the file does not exist for your service, please create one. You can refer the '
                    'MOVED_COMMANDS map in services/core/tests/extend_test_compute.py as an example.'
                    .format(
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_auto_scaling_policy.command_name', 'update'),
                        root_command_name, resource_group_command_name,
                        oci_cli.cli_util.override('update_auto_scaling_policy.command_name', 'update')))

            params.append('--force')
            params.extend(['--from-json', input_content])
            try:
                util.set_admin_pass_phrase()
                result = invoke(runner, config_file, 'ADMIN', params)

                message = cli_testing_service_client.validate_result(
                    'autoscaling',
                    'UpdateAutoScalingPolicy',
                    request_containers[i]['containerId'],
                    request_containers[i]['request'],
                    result,
                    'autoScalingPolicy',
                    False
                )
            finally:
                if os.path.exists('tests/resources/keyfile_for_test_update_auto_scaling_policy.pem'):
                    os.remove('tests/resources/keyfile_for_test_update_auto_scaling_policy.pem')
                if os.path.exists('tests/resources/config_for_test_update_auto_scaling_policy'):
                    os.remove('tests/resources/config_for_test_update_auto_scaling_policy')
                if cleanup:
                    try:
                        next(cleanup)
                    except StopIteration:
                        pass

            if message != "CONT":
                assert len(message) == 0, message
                done = True
            else:
                request_containers = cli_testing_service_client.get_requests(service_name='autoscaling', api_name='UpdateAutoScalingPolicy')
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
