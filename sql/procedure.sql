CREATE PROCEDURE `Verification`(
	IN `userID` VARCHAR(50),
	OUT `result` VARCHAR(50)
)
LANGUAGE SQL
NOT DETERMINISTIC
CONTAINS SQL
SQL SECURITY DEFINER
COMMENT ''
BEGIN

	DECLARE done, gg INT DEFAULT 0;
	DECLARE v_crush, v_user TEXT;
	DECLARE c_total CURSOR FOR SELECT recv , send FROM Crush WHERE notification = 0; 
	DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;
	
	OPEN c_total;
	
		REPEAT
			FETCH c_total INTO v_crush, v_user;
				IF done = 0 THEN
				
					IF v_crush = SHA2(userID, 224) THEN

                        SELECT IF(COUNT(*) > 0, TRUE, FALSE)
                        INTO gg
                        FROM Crush WHERE recv = (SELECT SHA2(username_id, 224) FROM Utilisateur WHERE SHA2(id, 224) = v_user)
						AND send = (SELECT SHA2(id, 224) FROM Utilisateur WHERE SHA2(username_id, 224) = v_crush)
						AND v_user <> (SELECT SHA2(id, 224) FROM Utilisateur WHERE username_id = userID)
						AND notification = 0;
						
											
						IF gg = TRUE THEN
							SELECT id INTO @cible FROM Utilisateur WHERE SHA2(id, 224) = v_user  ;
							SET result = @cible;
							SET done = 1;
						END IF;
						
					END IF;
				END IF; 
			UNTIL done
		END REPEAT;

	CLOSE c_total; 
	
	IF gg = FALSE THEN
		SET result = NULL;
	END IF;
	
END
