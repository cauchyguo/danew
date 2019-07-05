/*
SQL Data TransFer

Source Server		:MariaDB
Source Server Version	:10.3.15-MariaDB
Source Host		:cauchyguo.club
Source DataBase		:danew
Target Server 		:MariaDB
Target Server Version	:10.3.15-MariaDB
*/


use danew;
SET FOREIGN_KEY_CHECKS=0;
CREATE TABLE `Employee` (
  `employee_id` varchar(20) NOT NULL,
  `country` varchar(20)  NOT NULL,
  `gender` enum('male', 'female') NOT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
'Employee', {
    'employee_id': fields.String,
    'country': fields.String,
    'gender': fields.String(enum=['male', 'female']),

-- ----------------------------
-- Table structure for `users`

-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `userid` varchar(20) NOT NULL,
  `passwd` varchar(20)  NOT NULL,
  `authRank` varchar(20) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ---------------------------
-- Records of users
-- ---------------------------
INSERT INTO `users` VALUES('admin','admin','admin');
INSERT INTO `users` VALUES('白银御行','123456','client');
INSERT INTO `users` VALUES('四宫辉夜','234567','client');
INSERT INTO `users` VALUES('藤原千花','345678','client');
INSERT INTO `users` VALUES('石上优','345678','client');
INSERT INTO `users` VALUES('伊井野弥子','654321','client');


-- ----------------------------
-- Table structure for `packages`

-- ----------------------------
DROP TABLE IF EXISTS `packages`;
CREATE TABLE `packages` (
  `运单号` varchar(12) NOT NULL,
  `重量` float(5,3),
  `寄件人电话` varchar(11),
  `收件人电话` varchar(11),
  PRIMARY KEY (`运单号`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ---------------------------
-- Records of packages
-- ---------------------------
INSERT INTO `packages` VALUES('201901050001',10.30,'17777777777','18888888888');
INSERT INTO `packages` VALUES('201901050002',2.13,'18888888888','12333333333');
INSERT INTO `packages` VALUES('201901070001',4.44,'13777777777','13444444444');
INSERT INTO `packages` VALUES('201902050004',5.20,'15222222222','15777777777');


-- ----------------------------
-- Table structure for `orders`

-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `运单号` varchar(12) NOT NULL,
  `运费` float(5,2),
  `订单支付方电话` varchar(11),
  `订单支付状态` tinyint(1),
  PRIMARY KEY (`运单号`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ---------------------------
-- Records of orders
-- ---------------------------
INSERT INTO `orders` VALUES('201901050001',10.30,'17777777777',1);
INSERT INTO `orders` VALUES('201901050002',12.13,'18888888888',1);
INSERT INTO `orders` VALUES('201901070001',40.44,'13777777777',0);
INSERT INTO `orders` VALUES('201902050004',51.20,'15222222222',0);

