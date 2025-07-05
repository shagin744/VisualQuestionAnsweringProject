-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 21, 2024 at 12:48 PM
-- Server version: 5.6.12-log
-- PHP Version: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `vqadb`
--
CREATE DATABASE IF NOT EXISTS `vqadb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `vqadb`;

-- --------------------------------------------------------

--
-- Table structure for table `imagetable`
--

CREATE TABLE IF NOT EXISTS `imagetable` (
  `fid` int(11) NOT NULL,
  `emailid` varchar(50) NOT NULL,
  `fname` varchar(100) NOT NULL,
  `ptext` varchar(100) NOT NULL,
  `sdate` date NOT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `imagetable`
--

INSERT INTO `imagetable` (`fid`, `emailid`, `fname`, `ptext`, `sdate`) VALUES
(101, 'Sri@gmail.com', 'img8.jpg', 'img8.jpg', '2024-10-21');

-- --------------------------------------------------------

--
-- Table structure for table `usertable`
--

CREATE TABLE IF NOT EXISTS `usertable` (
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `cname` varchar(50) DEFAULT NULL,
  `mno` varchar(10) DEFAULT NULL,
  `emailid` varchar(50) NOT NULL,
  `pword` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`emailid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `usertable`
--

INSERT INTO `usertable` (`name`, `gender`, `age`, `address`, `cname`, `mno`, `emailid`, `pword`) VALUES
('Ajay', 'Male', 30, 'KK Nagar\r\nII Cross Street', 'Chennai', '9900990012', 'Ajay@gmail.com', 'Ajay'),
('Anu', 'Female', 25, 'Anna Nagar', 'Chennai', '9192939495', 'Anu@gmai.com', 'Anu'),
('Sri', 'Female', 20, 'Anna Nagar', 'Madurai', '9090909090', 'Sri@gmail.com', 'Sri');

-- --------------------------------------------------------

--
-- Table structure for table `videotable`
--

CREATE TABLE IF NOT EXISTS `videotable` (
  `fid` int(11) NOT NULL,
  `emailid` varchar(50) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `ptext` varchar(100) DEFAULT NULL,
  `sdate` date DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `videotable`
--

INSERT INTO `videotable` (`fid`, `emailid`, `fname`, `ptext`, `sdate`) VALUES
(1001, 'Sri@gmail.com', 'v13.mp4', 'v13.mp4', '2024-10-21');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
