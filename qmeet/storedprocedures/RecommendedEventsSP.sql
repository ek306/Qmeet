DELIMITER $$
CREATE DEFINER=`qmeet`@`%` PROCEDURE `RecommendedEventsSP`(
	IN Categories varchar(100)
)
BEGIN
	SET SQL_SAFE_UPDATES = 0;
	DELETE FROM qmeet.qmeet_selectedcategories;
	call SP_SplitString(Categories);
    
	select distinct qe.id, qe.title from qmeet_event qe
	join qmeet_eventcategories qec on qec.event_id = qe.id
	join qmeet_categories qc on qc.id = qec.categories_id
	where qc.category in (select * from qmeet.qmeet_selectedcategories);
END$$
DELIMITER ;
