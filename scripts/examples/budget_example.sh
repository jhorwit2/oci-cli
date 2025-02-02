#!/usr/bin/env bash
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.
# This script provides an example of how to use budgets and alert rules in the CLI in terms of:
#
#   - Managing budgets by performing create, read (get/list), update, delete operations on them
#   - Managing alert rules by performing create, read (get/list), update, delete operations on them
#
# Requirements for running this script:
#   - OCI CLI v2.5.3 or later (you can check this by running oci --version)
#   - jq (https://stedolan.github.io/jq/) for JSON querying and manipulation of CLI output. This may be a useful utility in general
#     and may help cater to scenarios which can't be wholly addressed by the --query option in the CLI
# Environment variables need to be set:
#   - COMPARTMENT_ID - The OCID of the compartment where the budget will be created. This must be your tenancy root compartment.
#   - TARGET_COMPARTMENT_ID - The OCID of the compartment that the budget will target.
#   - ALERT_RULE_RECIPIENT - The email address that the alert rule will send a message to when triggered.
# Environment variables that may optionally be set:
#   - BUDGET_AMOUNT - The budget amount. This should be a positive number.
#   - NEW_BUDGET_AMOUNT - The budget amount to be used in the update budget operation. This should be a positive number.

set -e

if [[ "$COMPARTMENT_ID" == "" ]]; then
    echo "COMPARTMENT_ID must be defined in your environment"
    exit 1
fi

if [[ "$TARGET_COMPARTMENT_ID" == "" ]]; then
    echo "TARGET_COMPARTMENT_ID must be defined in your environment"
    exit 1
fi

if [[ "$ALERT_RULE_RECIPIENT" == "" ]]; then
    echo "$ALERT_RULE_RECIPIENT must be defined in your environment"
    exit 1
fi

if [[ "$BUDGET_AMOUNT" == "" ]]; then
    BUDGET_AMOUNT=1050
fi

if [[ "$NEW_BUDGET_AMOUNT" == "" ]]; then
    NEW_BUDGET_AMOUNT=1105
fi

echo "Creating budget in compartment $COMPARTMENT_ID targeting compartment $TARGET_COMPARTMENT_ID with amount $BUDGET_AMOUNT"
CREATED_BUDGET=$(oci budgets budget create --compartment-id $COMPARTMENT_ID --target-compartment-id $TARGET_COMPARTMENT_ID --amount $BUDGET_AMOUNT --reset-period MONTHLY)

BUDGET_ID=$(jq -r '.data.id' <<< $CREATED_BUDGET)
echo "Getting budget $BUDGET_ID"
oci budgets budget get --budget-id $BUDGET_ID

echo "Listing budgets in compartment $COMPARTMENT_ID"
oci budgets budget list --compartment-id $COMPARTMENT_ID --limit 10

echo "Creating alert rule in budget $BUDGET_ID"
CREATED_ALERT_RULE=$(oci budgets alert-rule create --budget-id $BUDGET_ID --type FORECAST --threshold 100 --threshold-type PERCENTAGE --recipients $ALERT_RULE_RECIPIENT)

ALERT_RULE_ID=$(jq -r '.data.id' <<< $CREATED_ALERT_RULE)
echo "Getting alert rule $ALERT_RULE_ID"
oci budgets alert-rule get --alert-rule-id $ALERT_RULE_ID --budget-id $BUDGET_ID

echo "Listing alert rules in budget $BUDGET_ID"
oci budgets alert-rule list --budget-id $BUDGET_ID --limit 10

echo "Updating budget $BUDGET_ID to have amount $NEW_BUDGET_AMOUNT"
oci budgets budget update --budget-id $BUDGET_ID --amount $NEW_BUDGET_AMOUNT

echo "Updating alert rule $ALERT_RULE_ID to have type=ACTUAL, threshold=$BUDGET_AMOUNT, threshold-type=ABSOLUTE"
oci budgets alert-rule update --alert-rule-id $ALERT_RULE_ID --budget-id $BUDGET_ID --type ACTUAL --threshold $BUDGET_AMOUNT --threshold-type ABSOLUTE

echo "Deleting alert rule $ALERT_RULE_ID"
oci budgets alert-rule delete --alert-rule-id $ALERT_RULE_ID --budget-id $BUDGET_ID

# Deleting a budget results in deleting all of its alert rules as well, which in this case would have made the previous call redundant.
echo "Deleting budget $BUDGET_ID"
oci budgets budget delete --budget-id $BUDGET_ID
