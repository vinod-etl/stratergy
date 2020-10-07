USE `strategy_data`;

DROP TABLE IF EXISTS `stockdata`;
CREATE TABLE `stockdata` (
  `date` datetime NOT NULL,
  `zscore` varchar(45) NOT NULL,
  `stock_a` varchar(45) NOT NULL,
  `stock_b` varchar(45) NOT NULL,
  `beta` varchar(45) NOT NULL,
  `intercept` varchar(45) NOT NULL,
  `risk_ratio` varchar(45) NOT NULL,
  `pvalue` varchar(45) NOT NULL,
  `sector` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;