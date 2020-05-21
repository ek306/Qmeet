DELIMITER $$
CREATE DEFINER=`qmeet`@`%` PROCEDURE `GetFriendsSP`(
	IN UserID integer
)
BEGIN
	select qs2.id, qs2.username from qmeet_student qs 
	join qmeet_studentprofile qsp on qs.id = qsp.student_id
	join qmeet_studentprofile_friends qspf on qsp.id = qspf.from_studentprofile_id
	join qmeet_studentprofile qsp2 on qspf.to_studentprofile_id = qsp2.id
	join qmeet_student qs2 on qsp2.student_id = qs2.id
	where qs.id = UserID;
END$$
DELIMITER ;
