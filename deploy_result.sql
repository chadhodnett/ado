select
     ddr.id, ddr.status, ddr.delivery_id, ddr.environment_id, ddr.stack_id, dd.user_story
from delivery_data_deployresult ddr
join delivery_data_delivery dd on ddr.delivery_id = dd.id

select distinct dd.user_story
from delivery_data_delivery dd
join delivery_data_delivery_delivery_actions dda
on dda.delivery_id = dd.id
join delivery_data_action da
on da.id = dda.action_id
where da.name = 'Plsql'
and dd.id in (
    select id from delivery_data_delivery
    except
    select dd.id
    from delivery_data_delivery dd
    left join delivery_data_deployresult ddr
    on dd.id = ddr.delivery_id
    left join delivery_data_stack ds
    on ddr.stack_id = ds.id
    left join delivery_data_environment de
    on ddr.environment_id = de.id
    where dd.obsolete = 'f'
    and ddr.status = 'Pass'
    and ds.name = 'nsbb'
    and de.name = 'prod'
)
;

select distinct dd.user_story
from delivery_data_delivery dd
where dd.id in (
    select id from delivery_data_delivery
    except
    select dd.id
    from delivery_data_delivery dd
    left join delivery_data_deployresult ddr
    on dd.id = ddr.delivery_id
    left join delivery_data_stack ds
    on ddr.stack_id = ds.id
    left join delivery_data_environment de
    on ddr.environment_id = de.id
    where dd.obsolete = 'f'
    and ddr.status = 'Pass'
    and ds.name = 'sheet'
    and de.name = 'test'
)
;

select
     ddr.id, ddr.status, ddr.delivery_id, ddr.environment_id, ddr.stack_id, dd.user_story, da.name
from delivery_data_delivery dd
left join delivery_data_deployresult ddr
on dd.id = ddr.delivery_id
left join delivery_data_stack ds
on ddr.stack_id = ds.id
left join delivery_data_environment de
on ddr.environment_id = de.id
join delivery_data_delivery_delivery_actions dda
  on dda.delivery_id = dd.id
join delivery_data_action da
  on da.id = dda.action_id
where dd.obsolete = 'f'
and ddr.status = 'Pass'
and ds.name = 'nsbb'
and de.name = 'prod'
and da.name = 'Plsql'
;

select distinct dd.user_story
from delivery_data_delivery dd
where dd.id in (
    select dd.id
    from delivery_data_delivery dd
    left join delivery_data_deployresult ddr
    on dd.id = ddr.delivery_id
    left join delivery_data_stack ds
    on ddr.stack_id = ds.id
    join delivery_data_delivery_delivery_actions dda
    on dda.delivery_id = dd.id
    join delivery_data_action da
    on da.id = dda.action_id
    where dd.obsolete = 'f'
    and da.name = 'Plsql'
    and ds.name = 'nsbb'
    except
    select dd.id
    from delivery_data_delivery dd
    left join delivery_data_deployresult ddr
    on dd.id = ddr.delivery_id
    left join delivery_data_stack ds
    on ddr.stack_id = ds.id
    left join delivery_data_environment de
    on ddr.environment_id = de.id
    where dd.obsolete = 'f'
    and ddr.status = 'Pass'
    and ds.name = 'nsbb'
    and de.name = 'prod'
);