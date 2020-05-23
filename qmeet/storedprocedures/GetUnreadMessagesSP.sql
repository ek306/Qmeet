DELIMITER $$
CREATE DEFINER=`qmeet`@`%` PROCEDURE `GetUnreadMessagesSP`(
	IN UserID int(10)
)
BEGIN
	select count(*) as 'un_read', subject, sender_id from django_messages_message
	where read_at is null and recipient_id=UserID;
END$$
DELIMITER ;
