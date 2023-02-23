-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2023 at 04:40 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `faktury`
--

-- --------------------------------------------------------

--
-- Table structure for table `faktury`
--

CREATE TABLE `faktury` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cislo_faktury` tinytext NOT NULL,
  `dodavatel` tinytext NOT NULL,
  `odberatel` tinytext NOT NULL,
  `typ` tinyint(4) NOT NULL,
  `dodavatel_dph` tinyint(1) NOT NULL,
  `datum_vystaveni` date NOT NULL,
  `datum_zdanpl` date NOT NULL,
  `datum_splatnosti` date NOT NULL,
  `description_id` int(11) DEFAULT NULL,
  `mena` tinytext NOT NULL,
  `qr_platba` tinyint(1) NOT NULL,
  `vystaveno` tinytext NOT NULL,
  `je_sifrovano` tinyint(4) NOT NULL,
  `je_sablona` tinyint(1) NOT NULL,
  `variable_title0` tinytext DEFAULT NULL,
  `variable_data0` tinytext DEFAULT NULL,
  `variable_title1` tinytext DEFAULT NULL,
  `variable_data1` tinytext DEFAULT NULL,
  `variable_title2` tinytext DEFAULT NULL,
  `variable_data2` tinytext DEFAULT NULL,
  `variable_title3` tinytext DEFAULT NULL,
  `variable_data3` tinytext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `faktury`
--

INSERT INTO `faktury` (`id`, `user_id`, `cislo_faktury`, `dodavatel`, `odberatel`, `typ`, `dodavatel_dph`, `datum_vystaveni`, `datum_zdanpl`, `datum_splatnosti`, `description_id`, `mena`, `qr_platba`, `vystaveno`, `je_sifrovano`, `je_sablona`, `variable_title0`, `variable_data0`, `variable_title1`, `variable_data1`, `variable_title2`, `variable_data2`, `variable_title3`, `variable_data3`) VALUES
(38, 4, '20230201', '11', '12', 0, 0, '2023-01-31', '2023-01-24', '2023-01-24', NULL, 'czk', 0, '', 1, 0, '', '', '', '', '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `firmy`
--

CREATE TABLE `firmy` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `nazev` tinytext NOT NULL,
  `ico` tinytext NOT NULL,
  `dic` tinytext DEFAULT NULL,
  `ulice` tinytext NOT NULL,
  `cislo_popisne` tinytext NOT NULL,
  `mesto` tinytext NOT NULL,
  `psc` tinytext NOT NULL,
  `zeme` tinytext NOT NULL,
  `soud_rejstrik` tinytext NOT NULL,
  `soudni_vlozka` tinytext NOT NULL,
  `telefon` tinytext DEFAULT NULL,
  `email` tinytext DEFAULT NULL,
  `web` tinytext DEFAULT NULL,
  `cislo_uctu` tinytext DEFAULT NULL,
  `cislo_banky` tinytext DEFAULT NULL,
  `iban` tinytext DEFAULT NULL,
  `swift` tinytext DEFAULT NULL,
  `konst_symbol` tinytext DEFAULT NULL,
  `var_symbol` tinytext DEFAULT NULL,
  `je_odberatel` tinyint(1) NOT NULL,
  `je_dodavatel` tinyint(1) NOT NULL,
  `je_sifrovano` tinyint(1) NOT NULL,
  `smazano_uzivatelem` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `firmy`
--

INSERT INTO `firmy` (`id`, `user_id`, `nazev`, `ico`, `dic`, `ulice`, `cislo_popisne`, `mesto`, `psc`, `zeme`, `soud_rejstrik`, `soudni_vlozka`, `telefon`, `email`, `web`, `cislo_uctu`, `cislo_banky`, `iban`, `swift`, `konst_symbol`, `var_symbol`, `je_odberatel`, `je_dodavatel`, `je_sifrovano`, `smazano_uzivatelem`) VALUES
(11, 4, 'gAAAAABjzzDvqFl5vBsylsMvpjIAAx8xd-uFC6JZgWtFMyuJtm7vOG_TrOge8qPKFkav25hfVFfxuBBCf2jgC7QFIbinC3Nn4A==', 'gAAAAABjzzDvpSnLATiGYT3MhguEjnONfiefYJMB-9lE-th71xydKZ2AsP81KnyZZg7OypR1rhfvpEoz2RQmNmtsnAvGPUFyGA==', 'gAAAAABjzzDvN0qa45ResnCQFc6wbhPVyuaePE9MngH8ssQIj5ur9o0pfeqcOZqyxQFPZ7n0B-Jf-jE6VO3qhyKb4Chvxht0JA==', 'gAAAAABjzzDvvy__Wh1dX3BQfhb5ZqwzrSGTYY83HM96yudlbPYnJrqdjh4uWBWOBBnMqpy4qp4rx9FFxmzqR2K0RdCCTxi3wQ==', 'gAAAAABjzzDvQFd7MbnsIoigElvH6IDA9dqcqnj84KSndi9GAq-cKs9kv6A9i5pmDG6tK_PGl4yj7ZTQXNLIT5Wh8AeefTFURw==', 'gAAAAABjzzDvd_DWOTXrPtMhYWM43uzm1JD6W3FsPNXzg8Sa8i5x48SXatjIKyF5v1M4FvvzXtiX3YNO_pRvKM8MBDAL1Yu4GQ==', 'gAAAAABjzzDv17Xpywe7FDH88AR3RuuscqVual4fmfO340PxaMEmW33icbuQTD3XvC7bSSUxbZIl4KQqn7Lt-_JhHJJ6If3tHA==', 'gAAAAABjzzDvHx23WpCO8a2B2fF-dNuzIgVtZxrxr0VnCTkPusOFm-3enVjNszBW2tTJLKNTVxV4KDw2Oc7tu3fEdYnUJQtSdAhGmqY2MjIFuRd1BxipdJY=', 'gAAAAABjzzDvooyDpSgkJm8ftjvuqY3RqmWYk2oWu6t5SwqW-Pm8shf6DLSs1300J3W7YnBcc-19bhWN8iRt404fm15jNRw1btRaO41MEAEt-Spcirk7n9g=', 'gAAAAABjzzDvqSKfpBeinF5By1nZFrpSzyaz2v6h1rSTDBa7WvBGussHI7u-KOwSWz5GiyAAVj7kaG9a8tAW7b9zXwl0tAgRQA==', '', '', '', 'gAAAAABjzzDvMTf6zQnEHe3sQYxxW2nGVJG88nkuDsVO_760Z7W9bJTaw9HE8cjW7bVndlPEs8lB0AGapaVPNSsH9wdT4ve27g==', 'gAAAAABjzzDvhKxMFsAt7WhOKFDjtaPwEcO20hBGXfuD0xQ4epVvl1C4oQGJTKjJfwH2_T3nlhVJ12emodWsYVsnaycNCxfZIA==', '', '', '', '', 1, 1, 1, 0),
(12, 4, 'gAAAAABjzzD8QVIv-PW8ZxfPzqOANciudTdo5lnoLXwkzWuDqQswNH4uvm46jmp1fENzcelrdDYO6wqzFzuB9TUhYjxdtbVulQ==', 'gAAAAABjzzD8nENG9ov1GmvqAvrNaNshv1DURu5GG685HM-WsAfFZU-hHWDNVS5VvBsFUK9nT8xVRRDwPLTYARcv05Tt8IST6w==', 'gAAAAABjzzD8LpevATmO4wMXoqPV8X56XFzNvuEetV295sIZ32kRkFJl1FvLwWd8UqN4YaTTHP_AUMpb8NP8PS7FfrUfhZU_VQ==', 'gAAAAABjzzD8MKwXTpIPtI1Rg97IzEG5rpbjpVoeTMlhFnh33cB17ngbzsf2-eD_K2pfrQRkD3Yzog0VbPS4TO9rLhxBd3B8OA==', 'gAAAAABjzzD8AgAel-IhGondcOxAvtSNN7AJmQO-WB2m77tAUMEu31jfGgrS4GXexSWEUrnC-kTfmCh-vOqvoO4RNO0l6SdC0Q==', 'gAAAAABjzzD8m2nCGogjUYmFlaCEZ86dkpU-mi3708w2TzlnHslZmoOLLp7rzfN9Cm-V-n7t3mOxdjJCEbTrCCRLgKWLH2PwIA==', 'gAAAAABjzzD8LVYKKd6Qn1O6WkCEnEcQ7_TYWYO9_tJwFS6sBTlA8GU7642WKGKFRozIo-rFSz6UmTtNxI8M7ppXyEUyGmLoWw==', 'gAAAAABjzzD8AXacIiGgDFVam6Aqg0ZA3v6M7I5wS1OKomMJtYy1MOnsIxIz4Nlc4u7ReUxmhNtUtWDevpSOombbLCBPbuXU3JAHrhYSV3K6mOrTjDbDWa4=', 'gAAAAABjzzD84bXDR7Li3Jy0TIV2KYRLt_Su_36zasyAfwNAKov4EUGJ7ggiX5_T-cfAfsXqXot8H69zckiqyBfrwgVl50-3Fge0FTr9R6j4JgpAiM4niYcCJLbeR5_ZhpnGW38x-UA-', 'gAAAAABjzzD8FNS9aecO7k63p-46QIboLRcm_iC4YaHdcM4V6URIrRbgmnyecABashjOb7-QjRzBIX6qChvQGBpArou-iLULOg==', '', '', '', '', '', '', '', '', '', 1, 0, 1, 0),
(13, 4, 'gAAAAABjzzHy42VQT1M0bnsv73zefVtz0Eunj-ap1OFl3yUkUUP7Aj-0GvhxJGdsoSVug6xrSO8sRyf-g8WaQNSeHybPawa1NQ==', 'gAAAAABjzzHykIaypmwVoMByqGY_6yUfIJnPp4QZfhnJilHRHOTik2RqpamWE4C6tmdbdM_Feyqnl6FAas6kRNOkeEvXv3LWtg==', 'gAAAAABjzzHyx63cVcbkcBBfnDDyDVjl8-MRN-xmIB6a0NEmg9szyb5AIgxnZrc2K3qCAmHRdZvyR_bxS7ooSRX03Zp9CGPrNw==', 'gAAAAABjzzHyJdO1q-_9-JJ5cQATdBHsnXtTnqNUvVU2lTXMeW6o-Tn4ROGQQUfZWnwUrZsGlT9ZjBLibSXPP9aogwrxwvx7Jw==', 'gAAAAABjzzHytAKaDxcNRF_1Jj-zjvMoNJoq1ZKpC1P_j-U2aY_I7t19T2PHKQTuaDKaxhsUNFJPvIhJffqcdUtoLpJpC9QqvA==', 'gAAAAABjzzHym3T_v1p5Ae5o5i8ugXi2nC-ShrFOWnzfMiPPDx2suGuwiuH3dYNh-9xbXFcq_MSKiEk2CDfsKACws4q5RbVAog==', 'gAAAAABjzzHy2emcHwkdZUORco2Z_48PCCGa7I1J-zzmWNk1z4CL-xiQ1A6Gla8bBVEByJjG9ShyBaJ3paBJhV0kLZGwS3ajTw==', 'gAAAAABjzzHypa9frKJ8Z_vp0bQRZUcs_YAZnefXMzQBrFIkB7k2_aHrHNr4N3uwRkS1sIEkm-NDyYh-m7qWAZRJ4L47LiNxzycH8ew2GeAHjbJ-b3r5o7A=', 'gAAAAABjzzHyYgt0xBG8lG-3Tw6-Pm8mVLJjL0MFGtP8uz52smK6EB6ZEU_1UWdyVvclwXXVPW0UOUE3MB25wnP5XSU9tyOpCrCHAzbN-o6kThGWYfayEo4=', 'gAAAAABjzzHyegEjsBLGD34IWSpq2xLCDGNM_t5vlxrYI16r33Z4OqijKTdEMTWs7Sf5nWOFF-VX31zo8mkjH9ZVhqFHQicbEQ==', '', '', '', '', '', '', '', '', '', 0, 1, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `polozky`
--

CREATE TABLE `polozky` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `faktura_id` int(11) NOT NULL,
  `dodavka` tinytext NOT NULL,
  `dph` tinytext NOT NULL,
  `pocet` tinytext NOT NULL,
  `cena` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `polozky`
--

INSERT INTO `polozky` (`id`, `user_id`, `faktura_id`, `dodavka`, `dph`, `pocet`, `cena`) VALUES
(10, 4, 25, 'gAAAAABjzzAi9_LKepCHsu4U78cphjlFtNUD29XnZUl_pEkhMtej4R9NwQ2GZ7nAi0_Gs8MRSxxng6qHAldFiMZcLkvfR0ZljA==', 'gAAAAABjzzAiQc--Mqetpsu_O5vrWIGDI-OcDqAsTbG5MiO3l1x3LkDJBeukEDZ07sQOErgXry3r5SA3Xif5BZ-x-d5fIvNJfQ==', 'gAAAAABjzzAiMiSaJ4De9CJMn6FaxUd9sd3MzbRB6_BSSywk3y8pNTC0qkRS3tdfZ01BVzunWhjhg3DmwAm5NcbzY3VzJvtRyw==', 'gAAAAABjzzAixL6Xt0NFLfGp_rVb3Ge7WXNZi7JkauE07bkF-sxSTkT9YkpNcmbLS-iORuLFda9vOX0zHr1deb7sGqQuUMNyUQ=='),
(11, 4, 26, 'gAAAAABjzzEHSXEWFNkPr45U6_p94GcUx9SYWoNvFqJt3j16zw_uS9DdtNGUQJw1xhB6uauR4Xsv7RpqNNkVXt61AlwC8k0q-Q==', 'gAAAAABjzzEHAwcnZSQnVClgxx5as3FKGoFBB0a79fcwPgpHxyC0NxUDaoAST170LWBUc5SV1vTQVIGxGlUj68FZmmXqfDaXrw==', 'gAAAAABjzzEHMD_ezv9P4OvItZo0hTf4K_i73AhvfOeolXKo6hb3lqWUV5chybCYj0el4Y2hya0YwYFCXU7Zrz79UipVs71gmA==', 'gAAAAABjzzEHgeCEzZDmCXQA6PWKqPdXaIJMN4GLSp-b2S8_rtlf4GLqTqXBgoqthNmW48btSYvexWfN2fz5jP7vAcxStEiydw==');

-- --------------------------------------------------------

--
-- Table structure for table `popisky`
--

CREATE TABLE `popisky` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `nazev` tinytext NOT NULL,
  `popisek` text NOT NULL,
  `je_sifrovano` tinyint(1) NOT NULL,
  `smazano_uzivatelem` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sablony`
--

CREATE TABLE `sablony` (
  `sid` int(11) NOT NULL,
  `nazev` tinytext NOT NULL,
  `user_id` int(11) NOT NULL,
  `faktura_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(256) NOT NULL,
  `email` varchar(128) NOT NULL,
  `password` varchar(2048) NOT NULL,
  `data_key` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password`, `data_key`) VALUES
(4, 'walter', 'walter@seznam.cz', '$2b$12$qMIHIhubylOrJPovtWFkE.sIMGDC5NNXBq08OHBs1lyx3WX93xI9W', 'gAAAAABjzy-oI03R4ZQRmiN8BpNJ9tnrxnMtiQKwEFZTUpsOiVNr_vI9nAZNMPL5YGCSZbQe0oeNd5IbyiPPHSHYC5PGVnpwajUY8QQ7DoWgTMAYcuZ2u20yM38GAR_JkKmfNcTR51YJ');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `faktury`
--
ALTER TABLE `faktury`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `firmy`
--
ALTER TABLE `firmy`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `polozky`
--
ALTER TABLE `polozky`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `popisky`
--
ALTER TABLE `popisky`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sablony`
--
ALTER TABLE `sablony`
  ADD PRIMARY KEY (`sid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `faktury`
--
ALTER TABLE `faktury`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `firmy`
--
ALTER TABLE `firmy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `polozky`
--
ALTER TABLE `polozky`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `popisky`
--
ALTER TABLE `popisky`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sablony`
--
ALTER TABLE `sablony`
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
