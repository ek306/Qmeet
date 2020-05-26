SELECT * FROM qmeet.qmeet_studentprofile;DELIMITER $$
CREATE DEFINER=`qmeet`@`%` PROCEDURE `GetTimetableForUserSP`(
	IN StudentId integer
)
BEGIN
	SELECT 	qs.name as semester_name
	, 		qm.name as module_name
	,		qsm.start_hour
	,		qsm.end_hour
	,		LOWER(qsm.abbreviated_day) as abbreviated_day
	, 		qsm.end_hour - qsm.start_hour as duration 
	FROM qmeet.qmeet_semester qs
	JOIN qmeet.qmeet_semestermodule qsm ON qsm.semester_id = qs.id
	JOIN qmeet.qmeet_module qm ON qm.id = qsm.module_id
	JOIN qmeet.qmeet_coursemodules qcm ON qcm.module_id = qm.id
	JOIN qmeet.qmeet_studentprofile qsp ON qsp.course_id = qcm.course_id
	JOIN week_day_order wdo ON wdo.day = qsm.day
	WHERE qsp.student_id = StudentId
	ORDER BY qsm.start_hour, wdo.order;
END$$
DELIMITER ;
