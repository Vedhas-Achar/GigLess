-- GigLess schema export from Database_ddl_plsql.md
-- Generated on 2026-04-06

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;

CREATE DATABASE IF NOT EXISTS gigless
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE gigless;

CREATE TABLE IF NOT EXISTS accounts_user (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  password      VARCHAR(128)   NOT NULL,
  last_login    DATETIME(6)    NULL,
  is_superuser  TINYINT(1)     NOT NULL DEFAULT 0,
  username      VARCHAR(150)   NOT NULL,
  first_name    VARCHAR(150)   NOT NULL DEFAULT '',
  last_name     VARCHAR(150)   NOT NULL DEFAULT '',
  email         VARCHAR(254)   NOT NULL,
  is_staff      TINYINT(1)     NOT NULL DEFAULT 0,
  is_active     TINYINT(1)     NOT NULL DEFAULT 1,
  date_joined   DATETIME(6)    NOT NULL,
  -- custom fields
  name          VARCHAR(120)   NOT NULL,
  role          VARCHAR(20)    NOT NULL,                -- 'freelancer' | 'customer'
  bio           LONGTEXT       NOT NULL DEFAULT '',
  skills        LONGTEXT       NOT NULL DEFAULT '',
  profile_photo VARCHAR(100)   NULL DEFAULT NULL,       -- ImageField upload_to='profiles/'
  rating        DECIMAL(3,2)   NOT NULL DEFAULT 0.00,
  rating_count  INT UNSIGNED   NOT NULL DEFAULT 0,

  CONSTRAINT uk_accounts_user_username UNIQUE (username),
  CONSTRAINT uk_accounts_user_email    UNIQUE (email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS accounts_user_groups (
  id       BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id  BIGINT NOT NULL,
  group_id INT    NOT NULL,

  CONSTRAINT fk_aug_user  FOREIGN KEY (user_id)  REFERENCES accounts_user(id) ON DELETE CASCADE,
  CONSTRAINT fk_aug_group FOREIGN KEY (group_id) REFERENCES auth_group(id)    ON DELETE CASCADE,
  CONSTRAINT uk_aug_user_group UNIQUE (user_id, group_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS accounts_user_user_permissions (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id       BIGINT NOT NULL,
  permission_id INT    NOT NULL,

  CONSTRAINT fk_auup_user       FOREIGN KEY (user_id)       REFERENCES accounts_user(id)   ON DELETE CASCADE,
  CONSTRAINT fk_auup_permission FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
  CONSTRAINT uk_auup_user_perm  UNIQUE (user_id, permission_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS marketplace_services_category (
  id   BIGINT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,

  CONSTRAINT uk_msc_name UNIQUE (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS marketplace_services_service (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  freelancer_id BIGINT        NOT NULL,
  title         VARCHAR(180)  NOT NULL,
  description   LONGTEXT      NOT NULL,
  image         VARCHAR(100)  NULL DEFAULT NULL,       -- ImageField upload_to='services/'
  category_id   BIGINT        NOT NULL,
  price         DECIMAL(10,2) NOT NULL,
  delivery_time INT UNSIGNED  NOT NULL,                -- days
  created_at    DATETIME(6)   NOT NULL,                -- auto_now_add
  updated_at    DATETIME(6)   NOT NULL,                -- auto_now

  CONSTRAINT fk_mss_freelancer FOREIGN KEY (freelancer_id)
    REFERENCES accounts_user(id) ON DELETE CASCADE,
  CONSTRAINT fk_mss_category FOREIGN KEY (category_id)
    REFERENCES marketplace_services_category(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders_order (
  id                   BIGINT AUTO_INCREMENT PRIMARY KEY,
  customer_id          BIGINT      NOT NULL,
  service_id           BIGINT      NOT NULL,
  order_date           DATETIME(6) NOT NULL,           -- auto_now_add
  status               VARCHAR(20) NOT NULL DEFAULT 'pending',
                                                       -- 'pending' | 'in_progress' | 'completed'
  dummy_payment_status VARCHAR(20) NOT NULL DEFAULT 'paid',

  CONSTRAINT fk_oo_customer FOREIGN KEY (customer_id)
    REFERENCES accounts_user(id) ON DELETE CASCADE,
  CONSTRAINT fk_oo_service FOREIGN KEY (service_id)
    REFERENCES marketplace_services_service(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders_review (
  id         BIGINT AUTO_INCREMENT PRIMARY KEY,
  order_id   BIGINT           NOT NULL,
  rating     SMALLINT UNSIGNED NOT NULL,               -- 1â€“5
  comment    LONGTEXT         NOT NULL DEFAULT '',
  created_at DATETIME(6)      NOT NULL,                -- auto_now_add

  CONSTRAINT uk_or_order UNIQUE (order_id),
  CONSTRAINT fk_or_order FOREIGN KEY (order_id)
    REFERENCES orders_order(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS chat_conversation (
  id         BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_one_id BIGINT      NOT NULL,
  user_two_id BIGINT      NOT NULL,
  order_id    BIGINT      NULL DEFAULT NULL,
  created_at  DATETIME(6) NOT NULL,                    -- auto_now_add
  updated_at  DATETIME(6) NOT NULL,                    -- auto_now

  CONSTRAINT fk_cc_user_one FOREIGN KEY (user_one_id)
    REFERENCES accounts_user(id) ON DELETE CASCADE,
  CONSTRAINT fk_cc_user_two FOREIGN KEY (user_two_id)
    REFERENCES accounts_user(id) ON DELETE CASCADE,
  CONSTRAINT fk_cc_order FOREIGN KEY (order_id)
    REFERENCES orders_order(id) ON DELETE SET NULL,
  CONSTRAINT uniq_conversation_pair_order UNIQUE (user_one_id, user_two_id, order_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS chat_message (
  id              BIGINT AUTO_INCREMENT PRIMARY KEY,
  conversation_id BIGINT      NOT NULL,
  sender_id       BIGINT      NOT NULL,
  content         LONGTEXT    NOT NULL,
  is_read         TINYINT(1)  NOT NULL DEFAULT 0,
  created_at      DATETIME(6) NOT NULL,                -- auto_now_add

  CONSTRAINT fk_cm_conversation FOREIGN KEY (conversation_id)
    REFERENCES chat_conversation(id) ON DELETE CASCADE,
  CONSTRAINT fk_cm_sender FOREIGN KEY (sender_id)
    REFERENCES accounts_user(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Content types registry
CREATE TABLE IF NOT EXISTS django_content_type (
  id        INT AUTO_INCREMENT PRIMARY KEY,
  app_label VARCHAR(100) NOT NULL,
  model     VARCHAR(100) NOT NULL,
  UNIQUE (app_label, model)
) ENGINE=InnoDB;

-- Auth groups
CREATE TABLE IF NOT EXISTS auth_group (
  id   INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Auth permissions
CREATE TABLE IF NOT EXISTS auth_permission (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  name            VARCHAR(255) NOT NULL,
  content_type_id INT          NOT NULL,
  codename        VARCHAR(100) NOT NULL,
  CONSTRAINT fk_ap_ct FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE CASCADE,
  UNIQUE (content_type_id, codename)
) ENGINE=InnoDB;

-- Group â†” Permission M2M
CREATE TABLE IF NOT EXISTS auth_group_permissions (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  group_id      INT NOT NULL,
  permission_id INT NOT NULL,
  CONSTRAINT fk_agp_group FOREIGN KEY (group_id)      REFERENCES auth_group(id)      ON DELETE CASCADE,
  CONSTRAINT fk_agp_perm  FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
  UNIQUE (group_id, permission_id)
) ENGINE=InnoDB;

-- Admin log
CREATE TABLE IF NOT EXISTS django_admin_log (
  id              INT AUTO_INCREMENT PRIMARY KEY,
  action_time     DATETIME(6)   NOT NULL,
  object_id       LONGTEXT      NULL,
  object_repr     VARCHAR(200)  NOT NULL,
  action_flag     SMALLINT UNSIGNED NOT NULL,
  change_message  LONGTEXT      NOT NULL,
  content_type_id INT           NULL,
  user_id         BIGINT        NOT NULL,
  CONSTRAINT fk_dal_ct   FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE SET NULL,
  CONSTRAINT fk_dal_user FOREIGN KEY (user_id)         REFERENCES accounts_user(id)       ON DELETE CASCADE
) ENGINE=InnoDB;

-- Session store
CREATE TABLE IF NOT EXISTS django_session (
  session_key  VARCHAR(40)  PRIMARY KEY,
  session_data LONGTEXT     NOT NULL,
  expire_date  DATETIME(6)  NOT NULL,
  INDEX ix_django_session_expire (expire_date)
) ENGINE=InnoDB;

-- Migration tracking
CREATE TABLE IF NOT EXISTS django_migrations (
  id      BIGINT AUTO_INCREMENT PRIMARY KEY,
  app     VARCHAR(255) NOT NULL,
  name    VARCHAR(255) NOT NULL,
  applied DATETIME(6)  NOT NULL
) ENGINE=InnoDB;

-- Services
CREATE INDEX ix_mss_freelancer ON marketplace_services_service (freelancer_id);
CREATE INDEX ix_mss_category   ON marketplace_services_service (category_id);
CREATE INDEX ix_mss_price      ON marketplace_services_service (price);

-- Orders
CREATE INDEX ix_oo_customer ON orders_order (customer_id);
CREATE INDEX ix_oo_service  ON orders_order (service_id);
CREATE INDEX ix_oo_status   ON orders_order (status);

-- Reviews
CREATE INDEX ix_or_order ON orders_review (order_id);

-- Conversations
CREATE INDEX ix_cc_order ON chat_conversation (order_id);

-- Messages (composite for chat pagination)
CREATE INDEX ix_cm_conversation_created ON chat_message (conversation_id, created_at);

DELIMITER $$

CREATE FUNCTION fn_freelancer_avg_rating(p_freelancer_id BIGINT)
RETURNS DECIMAL(3,2)
READS SQL DATA
BEGIN
  DECLARE v_avg DECIMAL(3,2);

  SELECT IFNULL(ROUND(AVG(r.rating), 2), 0.00)
    INTO v_avg
    FROM orders_review r
    JOIN orders_order  o ON o.id = r.order_id
    JOIN marketplace_services_service s ON s.id = o.service_id
   WHERE s.freelancer_id = p_freelancer_id;

  RETURN v_avg;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE pr_create_order(
  IN  p_customer_id          BIGINT,
  IN  p_service_id           BIGINT,
  IN  p_dummy_payment_status VARCHAR(20),
  OUT p_order_id             BIGINT
)
BEGIN
  DECLARE v_freelancer_id BIGINT;

  SELECT freelancer_id
    INTO v_freelancer_id
    FROM marketplace_services_service
   WHERE id = p_service_id;

  IF v_freelancer_id = p_customer_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'You cannot order your own service.';
  END IF;

  INSERT INTO orders_order (customer_id, service_id, order_date, status, dummy_payment_status)
  VALUES (p_customer_id, p_service_id, NOW(6), 'pending', IFNULL(p_dummy_payment_status, 'paid'));

  SET p_order_id = LAST_INSERT_ID();
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE pr_update_order_status(
  IN p_order_id   BIGINT,
  IN p_actor_id   BIGINT,
  IN p_new_status VARCHAR(20)
)
BEGIN
  DECLARE v_customer_id   BIGINT;
  DECLARE v_freelancer_id BIGINT;

  SELECT o.customer_id, s.freelancer_id
    INTO v_customer_id, v_freelancer_id
    FROM orders_order o
    JOIN marketplace_services_service s ON s.id = o.service_id
   WHERE o.id = p_order_id;

  IF p_new_status NOT IN ('pending', 'in_progress', 'completed') THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Invalid status.';
  END IF;

  IF p_new_status = 'in_progress' AND p_actor_id <> v_freelancer_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Only freelancer can move order to in_progress.';
  END IF;

  IF p_new_status = 'completed' AND p_actor_id <> v_customer_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Only customer can complete order.';
  END IF;

  UPDATE orders_order
     SET status = p_new_status
   WHERE id = p_order_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE pr_recompute_freelancer_rating(
  IN p_freelancer_id BIGINT
)
BEGIN
  DECLARE v_avg DECIMAL(3,2);
  DECLARE v_cnt INT UNSIGNED;

  SELECT IFNULL(ROUND(AVG(r.rating), 2), 0.00), COUNT(*)
    INTO v_avg, v_cnt
    FROM orders_review r
    JOIN orders_order  o ON o.id = r.order_id
    JOIN marketplace_services_service s ON s.id = o.service_id
   WHERE s.freelancer_id = p_freelancer_id;

  UPDATE accounts_user
     SET rating       = v_avg,
         rating_count = v_cnt
   WHERE id = p_freelancer_id;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_conv_canonical_pair_bi
BEFORE INSERT ON chat_conversation
FOR EACH ROW
BEGIN
  DECLARE v_tmp BIGINT;

  IF NEW.user_one_id = NEW.user_two_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Conversation users must be different.';
  END IF;

  IF NEW.user_one_id > NEW.user_two_id THEN
    SET v_tmp = NEW.user_one_id;
    SET NEW.user_one_id = NEW.user_two_id;
    SET NEW.user_two_id = v_tmp;
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_conv_canonical_pair_bu
BEFORE UPDATE ON chat_conversation
FOR EACH ROW
BEGIN
  DECLARE v_tmp BIGINT;

  IF NEW.user_one_id = NEW.user_two_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Conversation users must be different.';
  END IF;

  IF NEW.user_one_id > NEW.user_two_id THEN
    SET v_tmp = NEW.user_one_id;
    SET NEW.user_one_id = NEW.user_two_id;
    SET NEW.user_two_id = v_tmp;
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_service_freelancer_role_bi
BEFORE INSERT ON marketplace_services_service
FOR EACH ROW
BEGIN
  DECLARE v_role VARCHAR(20);

  SELECT role INTO v_role
    FROM accounts_user
   WHERE id = NEW.freelancer_id;

  IF v_role <> 'freelancer' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Service owner must be freelancer.';
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_service_freelancer_role_bu
BEFORE UPDATE ON marketplace_services_service
FOR EACH ROW
BEGIN
  DECLARE v_role VARCHAR(20);

  SELECT role INTO v_role
    FROM accounts_user
   WHERE id = NEW.freelancer_id;

  IF v_role <> 'freelancer' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Service owner must be freelancer.';
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_order_customer_role_bi
BEFORE INSERT ON orders_order
FOR EACH ROW
BEGIN
  DECLARE v_role VARCHAR(20);

  SELECT role INTO v_role
    FROM accounts_user
   WHERE id = NEW.customer_id;

  IF v_role <> 'customer' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Order creator must be customer.';
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_order_customer_role_bu
BEFORE UPDATE ON orders_order
FOR EACH ROW
BEGIN
  DECLARE v_role VARCHAR(20);

  SELECT role INTO v_role
    FROM accounts_user
   WHERE id = NEW.customer_id;

  IF v_role <> 'customer' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Order creator must be customer.';
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_review_validation_bi
BEFORE INSERT ON orders_review
FOR EACH ROW
BEGIN
  DECLARE v_status VARCHAR(20);

  SELECT status INTO v_status
    FROM orders_order
   WHERE id = NEW.order_id;

  IF v_status <> 'completed' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Review allowed only for completed orders.';
  END IF;

  IF NEW.rating < 1 OR NEW.rating > 5 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Rating must be between 1 and 5.';
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_review_validation_bu
BEFORE UPDATE ON orders_review
FOR EACH ROW
BEGIN
  DECLARE v_status VARCHAR(20);

  SELECT status INTO v_status
    FROM orders_order
   WHERE id = NEW.order_id;

  IF v_status <> 'completed' THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Review allowed only for completed orders.';
  END IF;

  IF NEW.rating < 1 OR NEW.rating > 5 THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Rating must be between 1 and 5.';
  END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_review_recalc_ai
AFTER INSERT ON orders_review
FOR EACH ROW
BEGIN
  DECLARE v_freelancer_id BIGINT;

  SELECT s.freelancer_id
    INTO v_freelancer_id
    FROM orders_order o
    JOIN marketplace_services_service s ON s.id = o.service_id
   WHERE o.id = NEW.order_id;

  CALL pr_recompute_freelancer_rating(v_freelancer_id);
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_review_recalc_au
AFTER UPDATE ON orders_review
FOR EACH ROW
BEGIN
  DECLARE v_freelancer_id BIGINT;

  SELECT s.freelancer_id
    INTO v_freelancer_id
    FROM orders_order o
    JOIN marketplace_services_service s ON s.id = o.service_id
   WHERE o.id = NEW.order_id;

  CALL pr_recompute_freelancer_rating(v_freelancer_id);
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_review_recalc_ad
AFTER DELETE ON orders_review
FOR EACH ROW
BEGIN
  DECLARE v_freelancer_id BIGINT;

  SELECT s.freelancer_id
    INTO v_freelancer_id
    FROM orders_order o
    JOIN marketplace_services_service s ON s.id = o.service_id
   WHERE o.id = OLD.order_id;

  CALL pr_recompute_freelancer_rating(v_freelancer_id);
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER tr_message_touch_conversation_ai
AFTER INSERT ON chat_message
FOR EACH ROW
BEGIN
  UPDATE chat_conversation
     SET updated_at = NOW(6)
   WHERE id = NEW.conversation_id;
END$$

DELIMITER ;

INSERT INTO marketplace_services_category (name) VALUES
('Programming'),
('Design'),
('Writing'),
('Tutoring');

SET FOREIGN_KEY_CHECKS=1;

