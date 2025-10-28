# New AWS Services Added to enumerate-iam

This document lists all the new AWS services that have been added to the enumerate-iam tool's bruteforce tests.

## Summary

- **Total new services added**: 66
- **Total services now supported**: 205
- **File modified**: `enumerate_iam/bruteforce_tests.py`

## Services Added

The following AWS services and their operations have been added:

### 1. AI/ML and Bedrock Services
- **aiops** - 3 operations (list_applications, describe_applications, get_application)
- **bedrock** - 14 operations (list_custom_models, list_evaluation_jobs, list_foundation_models, list_guardrails, list_imported_models, list_inference_profiles, list_marketplace_model_endpoints, list_model_copy_jobs, list_model_customization_jobs, list_model_import_jobs, list_model_invocation_jobs, list_prompt_routers, list_provisioned_model_throughputs, get_model_invocation_logging_configuration)
- **bedrock-agent-runtime** - 1 operation (get_agent_memory)
- **bedrock-data-automation** - 2 operations (list_blueprints, list_data_automation_projects)
- **bedrock-data-automation-runtime** - 1 operation (get_data_automation_status)
- **qapps** - 2 operations (list_library_items, list_q_apps)
- **qconnect** - 2 operations (list_assistants, list_knowledge_bases)

### 2. Monitoring and Observability
- **application-signals** - 2 operations (list_service_level_objectives, get_service)
- **observabilityadmin** - 1 operation (list_resource_telemetry)
- **networkflowmonitor** - 2 operations (list_monitors, list_scopes)
- **networkmonitor** - 1 operation (list_monitors)
- **notifications** - 5 operations (list_channels, list_event_rules, list_notification_configurations, list_notification_events, list_notification_hubs)
- **notificationscontacts** - 1 operation (list_email_contacts)

### 3. Billing and Cost Management
- **billing** - 1 operation (list_billing_views)
- **bcm-pricing-calculator** - 4 operations (list_bill_estimates, list_bill_scenario_commitment_modifications, list_bill_scenario_usage_modifications, list_workload_estimate_usage)
- **cost-optimization-hub** - 3 operations (list_enrollment_statuses, list_recommendation_summaries, get_preferences)
- **freetier** - 1 operation (get_free_tier_usage)
- **taxsettings** - 1 operation (list_tax_registrations)

### 4. Security and Compliance
- **controlcatalog** - 4 operations (list_common_controls, list_controls, list_domains, list_objectives)
- **inspector-scan** - 2 operations (list_scans, get_scan_result)
- **pca-connector-scep** - 2 operations (list_challenge_metadata, list_connectors)
- **security-ir** - 2 operations (list_cases, list_memberships)
- **trustedadvisor** - 3 operations (list_checks, list_organization_recommendations, list_recommendations)

### 5. Networking and Geographic Services
- **arc-zonal-shift** - 2 operations (list_managed_resources, list_zonal_shifts)
- **geo-maps** - 3 operations (get_map_style_descriptor, get_sprites, get_tile)
- **geo-places** - 2 operations (get_place, list_keys)
- **geo-routes** - 1 operation (get_routes)
- **route53profiles** - 3 operations (list_profile_associations, list_profile_resource_associations, list_profiles)

### 6. Data and Storage Services
- **backupsearch** - 2 operations (list_search_jobs, list_search_result_export_jobs)
- **ds-data** - 1 operation (list_data_sets)
- **dsql** - 1 operation (list_clusters)
- **keyspaces** - 2 operations (list_keyspaces, list_tables)
- **neptune-graph** - 2 operations (list_graphs, list_private_graph_endpoints)
- **odb** - 1 operation (list_databases)
- **s3tables** - 2 operations (list_table_buckets, list_tables)
- **s3outposts** - 2 operations (list_endpoints, list_outposts_with_s3)
- **s3express** - 1 operation (list_express_one_zone_directories)
- **timestream-influxdb** - 2 operations (list_db_instances, list_db_parameter_groups)

### 7. Application and Development Services
- **apptest** - 3 operations (list_test_cases, list_test_configurations, list_test_runs)
- **deadline** - 4 operations (list_farms, list_fleets, list_queues, list_workers)
- **entityresolution** - 5 operations (list_id_mapping_workflows, list_id_namespaces, list_matching_workflows, list_provider_services, list_schema_mappings)
- **pcs** - 2 operations (list_clusters, list_queues)
- **repostspace** - 1 operation (list_spaces)

### 8. IoT and Media Services
- **iot-data** - 1 operation (list_named_shadows_for_thing)
- **iot1click-projects** - 1 operation (list_projects)
- **kinesis-video-webrtc-storage** - 1 operation (list_storage_configurations)
- **evs** - 1 operation (list_verification_jobs)
- **voice-id** - 1 operation (list_domains)

### 9. Messaging and Communication
- **mailmanager** - 9 operations (list_addon_instances, list_addon_subscriptions, list_archive_exports, list_archive_searches, list_archives, list_ingress_points, list_relay_rules, list_rule_sets, list_traffic_policies)
- **socialmessaging** - 1 operation (list_linked_whatsapp_business_accounts)

### 10. Marketplace Services
- **marketplace-agreement** - 1 operation (list_agreements)
- **marketplace-deployment** - 1 operation (list_deployment_parameters)
- **marketplace-reporting** - 1 operation (get_buyer_dashboard)
- **partnercentral-selling** - 1 operation (list_opportunities)

### 11. Medical and Healthcare
- **medical-imaging** - 2 operations (list_datastores, list_image_sets)
- **mpa** - 1 operation (list_privacy_budgets)

### 12. Systems Management and Operations
- **ssm-contacts** - 1 operation (list_contacts)
- **ssm-guiconnect** - 1 operation (list_connections)
- **ssm-incidents** - 2 operations (list_incident_records, list_response_plans)
- **ssm-quicksetup** - 1 operation (list_configuration_managers)
- **osis** - 1 operation (list_pipelines)

### 13. WorkSpaces and Desktop Services
- **workspaces-thin-client** - 3 operations (list_devices, list_environments, list_software_sets)
- **workspaces-web** - 7 operations (list_browser_settings, list_identity_providers, list_network_settings, list_portals, list_trust_stores, list_user_access_logging_settings, list_user_settings)

### 14. Other Services
- **sagemaker-edge** - 1 operation (get_device_registration)
- **sagemaker-metrics** - 1 operation (batch_get_metrics)
- **supplychain** - 3 operations (list_data_integration_flows, list_data_lake_datasets, list_instances)

## How the Tool Works

The enumerate-iam tool attempts to call AWS API operations that:
1. Don't require input parameters (or have all parameters as optional)
2. Are safe "read-only" operations (list, describe, get methods)
3. Help identify what IAM permissions are available to a given set of AWS credentials

## Usage

The tool can be run as before:

```bash
python enumerate-iam.py \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --region us-east-1
```

Or with session tokens:

```bash
python enumerate-iam.py \
  --access-key YOUR_ACCESS_KEY \
  --secret-key YOUR_SECRET_KEY \
  --session-token YOUR_SESSION_TOKEN \
  --region us-east-1
```

## Notes

- Some services may not be available in all AWS regions
- Some operations may require specific service endpoints or configurations
- The tool will automatically handle services that are not available in the specified region
- Operations that fail due to permissions or unavailability will be logged but won't stop the enumeration process

## Reference

Based on AWS CLI documentation, particularly the [Bedrock service reference](https://docs.aws.amazon.com/cli/latest/reference/bedrock/).

