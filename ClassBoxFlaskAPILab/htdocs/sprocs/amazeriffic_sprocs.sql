-- drop procedure get_todos;

delimiter //
create procedure get_todos(IN in_userId int, IN in_description varchar(100))
begin
declare v_userId int;
declare v_description varchar(100);

IF in_userId = ''  or in_userId IS NULL THEN 
	SET v_userId = 1; 
ELSE
	SET v_userId = in_userId;
END IF;

IF in_description = '' THEN
	SET v_description = '%';
ELSE
	SET v_description = in_description;
END IF;
	
select tt.description, t.tagName, tasks.userId , r.CUDDate
from tasks 
join taskTypes tt on tt.taskTypeId = tasks.taskTypeId 
join tags t on t.tagId = tasks.tagId
join (select it.taskTypeId, it.userId, max(it.CUDDate) as CUDDate from tasks it where it.userId = 1 group by it.taskTypeId, it.userId) r on r.taskTypeId = tasks.taskTypeId and r.userId = tasks.userId
where tasks.userId = 1 and tt.description like v_description
order by  r.CUDDate  ;

end //
delimiter ;
-- e.g. 
-- CALL get_todos(1, '');

-----------------------------------------------------------
 
-- drop procedure create_todos;
delimiter //
create procedure create_todos(IN in_userId int, IN in_description varchar(100), in_tagName varchar(100))
begin

declare v_userId int;
declare v_taskTypeId int ;
declare v_tagId int ;
set v_taskTypeId = null;
set v_tagId = null;

IF in_userId = '' THEN 
	SET v_userId = 1; 
ELSE
	SET v_userId = in_userId;
END IF;

select t.taskTypeId 
into v_taskTypeId 
from taskTypes t 
where t.description = in_description;

if (v_taskTypeId is null) then
	insert into taskTypes (description, CUDAction) values (in_description, 1);
	set v_taskTypeId = LAST_INSERT_ID();
end if ;

select t.tagId  
into v_tagId 
from tags t 
where t.tagName = in_tagName;

if (v_tagId is null) then
	insert into tags (tagName, CUDAction) values (in_tagName, 1);
	set v_tagId = LAST_INSERT_ID();
end if;

-- Add new record, but prevent inserting duplicate record:
INSERT INTO tasks (taskTypeId, tagId, userId, CUDAction) 
SELECT v_taskTypeId, v_tagId, v_userId, 1 
FROM (SELECT v_taskTypeId, v_tagId, v_userId) AS tmp
WHERE NOT EXISTS (
    SELECT taskTypeId, TagId, userId 
    FROM tasks 
    WHERE userId = v_userId and taskTypeId = v_taskTypeId and tagId = v_tagId
) LIMIT 1;
 
end //

delimiter ;

-- e.g.:
-- CALL create_todos (1, 'pilates', 'chores');
-- CALL create_todos (1, 'shopping', 'chores');

-----------------------------

-- drop procedure delete_todo;
delimiter //
create procedure delete_todo(IN in_userId int, IN in_description varchar(100))
begin

declare v_userId int;
declare v_taskTypeId int;
set v_taskTypeId = null;

IF in_userId = '' THEN 
	SET v_userId = 1; 
ELSE
	SET v_userId = in_userId;
END IF;

select t.taskTypeId 
into v_taskTypeId 
from taskTypes t 
where t.description = in_description;

IF (v_taskTypeId is not null) THEN
	DELETE FROM tasks 
	WHERE taskTypeId = v_taskTypeId and userId = v_userId;
END IF;

end //

delimiter ;

-- e.g.:
-- CALL delete_todo (1, 'pilates');


