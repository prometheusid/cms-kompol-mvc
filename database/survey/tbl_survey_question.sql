-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 05, 2022 at 06:57 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_kompol`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_survey_question`
--

CREATE TABLE `tbl_survey_question` (
  `id_survey_question` int(10) NOT NULL,
  `code` varchar(50) NOT NULL,
  `question` text NOT NULL,
  `variabel` varchar(100) NOT NULL,
  `created_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_survey_question`
--

INSERT INTO `tbl_survey_question` (`id_survey_question`, `code`, `question`, `variabel`, `created_date`) VALUES
(9, 'q768', 'Seberapa Kenal dengan mereka? ', '2', '2022-02-05 12:49:13');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_survey_question`
--
ALTER TABLE `tbl_survey_question`
  ADD PRIMARY KEY (`id_survey_question`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_survey_question`
--
ALTER TABLE `tbl_survey_question`
  MODIFY `id_survey_question` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
