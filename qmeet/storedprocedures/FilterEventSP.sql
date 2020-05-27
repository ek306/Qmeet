DELIMITER $$
CREATE DEFINER=`qmeet`@`%` PROCEDURE `FilterEventSP`(
	IN Title varchar(50),
    IN Categories varchar(50)
)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
	DELETE FROM qmeet.qmeet_selectedcategories;
	call SP_SplitString(Categories);
    
    IF(Title <> '' AND Categories = '') 
    THEN
		select * from qmeet.qmeet_event qe
        where qe.title like concat("%", Title, "%");
        
	ELSEIF(Title <> '' AND Categories <> '')
    THEN
		select distinct qe.id, qe.title from qmeet_event qe
		join qmeet_eventcategories qec on qec.event_id = qe.id
		join qmeet_categories qc on qc.id = qec.categories_id
		where qc.category in (select * from qmeet.qmeet_selectedcategories)
        and qe.title like concat("%", Title, "%");
	
    ELSE
		select distinct qe.id, qe.title from qmeet_event qe
		join qmeet_eventcategories qec on qec.event_id = qe.id
		join qmeet_categories qc on qc.id = qec.categories_id
		where qc.category in (select * from qmeet.qmeet_selectedcategories);
	END IF;
END$$
DELIMITER ;
