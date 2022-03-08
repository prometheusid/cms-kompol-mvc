-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 08, 2022 at 05:33 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.4.24

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
-- Table structure for table `info`
--

CREATE TABLE `info` (
  `info_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `judul_info` varchar(255) DEFAULT NULL,
  `isi_info` text DEFAULT NULL,
  `thumb` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `info`
--

INSERT INTO `info` (`info_id`, `user_id`, `judul_info`, `isi_info`, `thumb`, `created_at`) VALUES
(28, 30, 'Vaksin Ke 2 Untuk Guru dan Karyawan SD/MI Pundong', '<p><span style=\"color: rgb(34, 34, 34); font-family: &quot;Droid Serif&quot;, sans-serif, Helvetica, Arial; font-size: 16px; background-color: rgb(255, 255, 255);\">Vaksin tahap ke 2 untuk guru dan karyawan Sekolah Dasar di lingkungan Kapanewon Pundong dilakukan di lingkungan kapanewon, Senin (5/4). Semua petugas dari Puskesmas Pundong telah disiapkan sejak pagi dibantu dari Polsek dan Koramil Pundong untuk membantu mengatasi antrian.Dari data yang diundang sebanyak 180 orang yang hadir 179 dan satu orang baru dalam keadaan sakit. (Dib).</span><br></p>', 'img730_IMG_20210405_083500.jpg', '2022-03-08 11:19:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `info`
--
ALTER TABLE `info`
  ADD PRIMARY KEY (`info_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `info`
--
ALTER TABLE `info`
  MODIFY `info_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
