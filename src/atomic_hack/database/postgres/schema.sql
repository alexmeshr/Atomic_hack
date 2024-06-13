-- добавляем расширение pgvector
create extension vector;

create table support_chat (
     session_id uuid                                            -- айдишник сессии
    -- ,client_id int                                           -- хз что сюда писать и зачем
    ,message_id uuid                                            -- айдишник сообщения (автоинкрементируется)
    ,sender text                                 not null       -- либо `from_user` либо `from_support`
    ,message text                                not null       --  само сообщение
    ,message_dttm timestamp without time zone    default now()  -- время получения сообщения
    ,meta json                                   default null   -- кто / кого / куда / откуда (пусть будет)
);
