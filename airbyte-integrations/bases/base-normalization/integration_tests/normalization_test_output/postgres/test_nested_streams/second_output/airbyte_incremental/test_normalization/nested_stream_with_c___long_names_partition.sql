
      delete
    from "postgres".test_normalization."nested_stream_with_c___long_names_partition"
    where (_airbyte_ab_id) in (
        select (_airbyte_ab_id)
        from "nested_stream_with_c___long_names_partitio__dbt_tmp"
    );

    insert into "postgres".test_normalization."nested_stream_with_c___long_names_partition" ("_airbyte_nested_stre__nto_long_names_hashid", "double_array_data", "DATA", "_airbyte_ab_id", "_airbyte_emitted_at", "_airbyte_normalized_at", "_airbyte_partition_hashid")
    (
       select "_airbyte_nested_stre__nto_long_names_hashid", "double_array_data", "DATA", "_airbyte_ab_id", "_airbyte_emitted_at", "_airbyte_normalized_at", "_airbyte_partition_hashid"
       from "nested_stream_with_c___long_names_partitio__dbt_tmp"
    );
  