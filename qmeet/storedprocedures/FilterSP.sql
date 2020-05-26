DELIMITER $$
CREATE DEFINER=`qmeet`@`%` PROCEDURE `FilterSP`(
	IN Username varchar(50),
    IN Categories varchar(50)
)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
	DELETE FROM qmeet.qmeet_selectedcategories;
	call SP_SplitString(Categories);
    
	IF(Username <> '' AND Categories = '')
    THEN 
		SELECT qs.id, qs.username from qmeet.qmeet_studentProfile qsp
		join qmeet.qmeet_student qs on qs.id = qsp.student_id
		where qs.username LIKE concat("%", Username, "%");
        
    ELSEIF(Username <> '' AND Categories <> '')
    THEN
		select distinct qs.id, qs.username from qmeet.qmeet_studentcategories qsc
		join qmeet.qmeet_categories qc on qc.id = qsc.categories_id
		left join qmeet.qmeet_studentprofile qsp on qsp.id = qsc.student_profile_id
		left join qmeet.qmeet_student qs on qs.id = qsp.student_id
		where qc.category in (select * from qmeet.qmeet_selectedcategories)
		and qs.username LIKE concat("%", Username, "%");
    
    ELSE
		select distinct qs.id, qs.username from qmeet.qmeet_studentcategories qsc
		join qmeet.qmeet_categories qc on qc.id = qsc.categories_id
		left join qmeet.qmeet_studentprofile qsp on qsp.id = qsc.student_profile_id
		left join qmeet.qmeet_student qs on qs.id = qsp.student_id
		where qc.category in (select * from qmeet.qmeet_selectedcategories);
	END IF;
END$$
DELIMITER ;
