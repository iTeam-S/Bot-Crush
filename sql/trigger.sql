
CREATE  TRIGGER `Tache_donnee`
  BEFORE UPDATE ON `Tache` FOR EACH ROW BEGIN
    IF NEW.fini = 1 THEN 
      SET NEW.donnee = NULL;
    END IF ;
END
