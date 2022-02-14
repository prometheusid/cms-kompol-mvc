-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 14, 2022 at 04:36 AM
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
-- Table structure for table `tbl_lapkun`
--

CREATE TABLE `tbl_lapkun` (
  `lapkun_id` int(11) NOT NULL,
  `lapkun_judul` varchar(255) NOT NULL,
  `lapkun_isi` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_lapkun`
--

INSERT INTO `tbl_lapkun` (`lapkun_id`, `lapkun_judul`, `lapkun_isi`, `user_id`, `created_at`) VALUES
(1, 'Tes Laporan Kunjungan', 'Ini adalah tes laporan kunjungan yang diisi lagsung via sql', 30, '2022-02-14 04:11:53'),
(2, 'tes tambah laporan', '<p><span style=\"background-color: rgb(255, 255, 0);\">tes isi laporan</span></p>', 30, '2022-02-14 10:32:46');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_lapkun`
--
ALTER TABLE `tbl_lapkun`
  ADD PRIMARY KEY (`lapkun_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_lapkun`
--
ALTER TABLE `tbl_lapkun`
  MODIFY `lapkun_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
