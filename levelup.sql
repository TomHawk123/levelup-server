SELECT g.id,
  g.game_type_id,
  g.title,
  g.maker,
  g.gamer_id,
  g.number_of_players,
  g.skill_level,
  t.label game_type
FROM levelupapi_game g
  LEFT JOIN levelupapi_gametype t ON g.game_type_id = t.id
WHERE t.id = 2
SELECT le.id,
  le.date,
  le.time,
  lg.title as game_name,
  au.first_name || " " || au.last_name as full_name
FROM levelupapi_event le
  JOIN levelupapi_gamer lgr ON lgr.id = le.organizer_id
  JOIN auth_user au ON au.id = lgr.user_id
  JOIN levelupapi_game lg ON le.game_id
SELECT lg.id,
  lg.title,
  lg.maker,
  lg.skill_level,
  lg.number_of_players,
  lg.game_type_id,
  lg.gamer_id,
  au.first_name || " " || au.last_name as full_name
FROM levelupapi_game lg
  JOIN levelupapi_gamer lgr ON lgr.id = lg.gamer_id
  JOIN auth_user au ON au.id = lgr.id

SELECT le.id,
  le.date,
  le.time,
  lg.title as game_name,
  au.first_name || " " || au.last_name as attending_gamer_name
FROM levelupapi_event le
  JOIN levelupapi_gamer lgr ON lgr.id = le.organizer_id
  JOIN auth_user au ON au.id = lgr.user_id
  JOIN levelupapi_game lg ON le.game_id