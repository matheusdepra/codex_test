{{ config(materialized='view') }}

select
  1 as id,
  'exemplo' as descricao,
  current_timestamp as created_at
