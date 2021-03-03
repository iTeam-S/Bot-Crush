-- --------------------------------------------------------
-- Hôte:                         ---
-- Version du serveur:           10.3.25-MariaDB-0ubuntu0.20.04.1 - Ubuntu 20.04
-- SE du serveur:                debian-linux-gnu
-- HeidiSQL Version:             11.1.0.6116
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Listage de la structure de la procédure bot_crush. Verification
DELIMITER //
CREATE PROCEDURE `Verification`(
	IN `userID` VARCHAR(50)
)
BEGIN

	DECLARE done, gg INT DEFAULT 0;
	DECLARE v_crush, v_user, v_user_crypt TEXT;
	DECLARE c_total CURSOR FOR SELECT username_crush, id_utilisateur FROM Crush WHERE notification = 0; 
	DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;
	
	OPEN c_total;
	
		REPEAT
			FETCH c_total INTO v_crush, v_user;
				IF done = 0 THEN
				
					IF v_crush = SHA2(userID, 224) THEN
						SELECT SHA2(id_username, 224) INTO v_user_crypt FROM Utilisateur WHERE id_fb = v_user;
						
						SELECT 
							CASE 
								WHEN COUNT(*)>0 THEN TRUE ELSE FALSE
							END INTO gg
						FROM Crush WHERE username_crush = v_user_crypt
						AND notification = 0
						AND id_utilisateur = ( SELECT id_fb FROM Utilisateur WHERE id_username = userID);
											
						IF gg = TRUE THEN
							SELECT True AS Statut, v_user AS Cible ;
							SET done = 1;
						END IF;
						
					END IF;
				END IF; 
			UNTIL done
		END REPEAT;

	CLOSE c_total; 
	
	IF gg = FALSE THEN
		SELECT False AS Statut, NULL AS Cible ;
	END IF;
	
END//
DELIMITER ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
