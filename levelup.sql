SELECT *
FROM levelupapi_gametype;
SELECT *
FROM auth_user;
SELECT *
FROM authtoken_token;
SELECT *
FROM levelupapi_gamer;
DROP TABLE levelupapi_game
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
