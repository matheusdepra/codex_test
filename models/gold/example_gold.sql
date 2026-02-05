{{ config(materialized='table') }}

select
  id,
  descricao,
  count(*) as total_registros,
  max(created_at) as ultima_atualizacao
from {{ ref('example_silver') }}
group by id, descricao
