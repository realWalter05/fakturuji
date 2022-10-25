-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 25, 2022 at 11:33 PM
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
  `qr_platba` tinyint(1) NOT NULL,
  `vystaveno` tinytext NOT NULL,
  `je_sifrovano` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `faktury`
--

INSERT INTO `faktury` (`id`, `user_id`, `cislo_faktury`, `dodavatel`, `odberatel`, `typ`, `dodavatel_dph`, `datum_vystaveni`, `datum_zdanpl`, `datum_splatnosti`, `qr_platba`, `vystaveno`, `je_sifrovano`) VALUES
(18, 1, '2029228', '48', '40', 0, 1, '2022-10-22', '2022-10-22', '2022-10-22', 0, 'Zíka Václav', 0),
(19, 1, '2029228', '48', '40', 0, 0, '2022-11-06', '2022-10-20', '2022-10-22', 0, 'Pavel Dvořák', 0),
(20, 1, '2022005', '48', '40', 0, 1, '2022-10-22', '2022-10-22', '2022-10-22', 1, 'Zíka Václav', 0),
(21, 1, '2022005', '49', '41', 0, 1, '2022-10-22', '2022-10-22', '2022-10-22', 0, 'Václav Zíka', 0),
(22, 1, '2022001', '50', '51', 0, 1, '2022-11-24', '2022-10-24', '2022-10-24', 1, 'Pan Příkladný', 0),
(23, 1, '2022001', '50', '51', 0, 0, '2022-12-06', '2022-10-24', '2022-10-24', 0, '', 1),
(24, 1, '2022001', '50', '51', 0, 0, '2022-12-06', '2022-10-24', '2022-10-24', 0, '', 1),
(25, 1, '2022001', '50', '51', 0, 0, '2022-12-06', '2022-10-24', '2022-10-24', 0, '', 1),
(26, 1, '2022001', '48', '51', 0, 0, '2022-10-24', '2022-10-24', '2022-10-24', 1, 'Zíka Václav', 1),
(27, 1, '2022001', '48', '42', 0, 0, '2022-10-24', '2022-10-24', '2022-10-24', 1, 'Zíka Václav', 0),
(28, 1, '2022001', '48', '42', 0, 0, '2022-10-24', '2022-10-24', '2022-10-24', 1, 'Zíka Václav', 0),
(29, 1, '2022001', '48', '42', 0, 0, '2022-10-24', '2022-10-24', '2022-10-24', 1, 'Zíka Václav', 1),
(30, 2, '', '44', '38', 0, 0, '2022-10-25', '2022-10-25', '2022-10-25', 1, '', 0),
(31, 2, '', '44', '44', 0, 0, '2022-10-25', '2022-10-25', '2022-10-25', 0, '', 0);

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
  `je_sifrovano` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `firmy`
--

INSERT INTO `firmy` (`id`, `user_id`, `nazev`, `ico`, `dic`, `ulice`, `cislo_popisne`, `mesto`, `psc`, `zeme`, `soud_rejstrik`, `soudni_vlozka`, `telefon`, `email`, `web`, `cislo_uctu`, `cislo_banky`, `iban`, `swift`, `konst_symbol`, `var_symbol`, `je_odberatel`, `je_dodavatel`, `je_sifrovano`) VALUES
(38, 2, 'Alza.cz a.s.', '27082440', 'CZ27082440', 'Jankovcova', '1522', 'Praha', '17000', 'Česká republika', 'Městský soud v Praze', 'B 8573', '', '', '', '', '', '', '', '', '', 1, 1, 0),
(40, 1, 'gAAAAABjSusaMfN8zFy3PduoSYVkpQnYEIurggPUqcsdIHCul_IlYoY16GpAqPfStzdGr1KQWXWzkM2_d-Fgqj3nXsRZ1lfdDkY1eZgo08w_7kWaQkLJY_Sj-Q0UoI91jADQFXH2CzzE', 'gAAAAABjSusaL-LMnMC9D2uCfRDdL7Yt-zgFY86KO8feVCQzPoUdSJ5is0y2xWSuKdS5xhkmtsBQR50mu1y3FODA-JteFWb3SA==', 'gAAAAABjSusab-oY7pMt64D3_xXgv0LYiNHS2MUGkQbKA6HigE09DRXy2JzABNRKIQe_YOaUf6-cKAVU5eWKi3mdzuVePNmh0g==', 'gAAAAABjSusapMcNS96jpfIR6i16Of8c7Hvw_4AhpfuNz2lnedvSKOTfTDeN3Ta5edPFT-SA5dRqSeCEllRrEyQ5QqoKohVhvg==', 'gAAAAABjSusahytQxnAIBgCOfTPnDrYsv49qMADpAd1D3i5oHs17_dqIHSipJMqFoMSTLu2iapw6NPB5eh04HFTVn5xo7uq_vA==', 'gAAAAABjSusaYuxgk5nKf62NDirEmDYHizNCjwgtbNu7hKAXocDVrCwAUGVP_tGp8HCQeHk4Z5AkR3_TT3bzFqY7h5ybA0tV-g==', 'gAAAAABjSusaYv45kV85fW-XvQ0XK6nLXfxhG4AFyz_ChiD6m-fB-Y15r-8sNe015GnmO1XudBZ-WA61Vd2-lct_4IjbCCbeYQ==', 'gAAAAABjSusag2y4ApcSzjYkpqNI-GKkPSiP6RjHCWMCUyZI9sC_MYVMWJd21NfuJgEh0nwdCE_L81loJHofgNpN0xkYZHzCliGPPRPaI-xTJ5HCJ8ieRxA=', 'gAAAAABjSusasbwtJb3K1VTNF49gxYQ2Tn6fmnacAm1t7Mu-cXXZQm_Lxn8IDG0sgwZBmctFoSUhn0VlsykKNvQRzfOWRzZmGxG1d57G8mdivRoR4x7wknk=', 'gAAAAABjSusapuMRpjdkp2CEaQUXLHC6MLrn5WsUXskoP8tmLg3FqIYotKCtS3pyvzNR9E5PACyEvJUKDGH6SOMBR78BneWyQg==', 'gAAAAABjSusacOIpjFhEW3I5NYAAjJEVbrqZ4k2ztG8XR9E80woRMuWhwLHoJiKihUPhXVGi6F2zGZdxdh41D56JpdpRcj1HSg==', '', '', 'gAAAAABjSusauIFXrvVgDmIjlakHF2h3nlWRP0_6cXxPx2kTH6Yv7xW8LYJ6RcNHgMALl8XriX6lvxJBiC7W7JtLEApE5yJsXw==', 'gAAAAABjSusavvDSObkmtJOScVmlG6ykx7CFzwp7Es6ELmLHeq1g21s_mRxCjv6cjUktq1Xwektj2ImZcAnc7yAO3w9cNhN30g==', '', '', '', '', 1, 0, 1),
(41, 1, 'Happy Technik s.r.o.', '26069156', 'CZ26069156', '', '64', 'Vrcovice', '39701', 'Česká republika', 'Krajský soud v Českých Budějovicích', 'C 12020', '', '', '', '', '', '', '', '', '', 1, 0, 0),
(42, 1, 'DORSIMO s.r.o.', '04501616', 'CZ04501616', 'Táborská', '496', '39701', 'Písek', 'Česká republika', 'Krajský soud v Českých Budějovicích', 'C 24195', '', '', '', '', '', '', '', '', '', 1, 0, 0),
(43, 1, 'gAAAAABjTYHhNvoSKNrNFPAZ3-qzJ3LEg_TRc9XOMTEg-ddyGpaKoGktHWcLpf67wI0vXGdrlBQU1Wmx9hoCdqrXh6y75jFKag==', 'gAAAAABjTYHhP9soR8PSx6inMNfJMQ8kp_6Jan87S0hc1lYXwuYwyLGlq-SAS-3BKQfiH_BJB2WvbgXkTBAP9JZTSbUOp5Y6GQ==', 'gAAAAABjTYHh5u2ewA59o9khRjth3prFKR3_uOD7kN0dOKawMlSNPqbwfj2yFy9ZmL9uNHHb_WdprPHWkBnDpl_xzR8gyZNfGw==', 'gAAAAABjTYHhSOTztvsmL1uy9VND-1rBIHb7OhXCI19l3djiC8tvd-I4lXbf6SB81nbwdMh0iXxYOl0kLEOI152WO0rcligdNg==', 'gAAAAABjTYHh6nPt_SilX19M3R7xWezWDHsn3PLFX2i_KYNeTeR94mDdL6Y4b6CMjbfC3LdkB1j34wlr_ibZI-NRo9QeU79Z4w==', 'gAAAAABjTYHhd3mUjppEdh2IgXN63-BphZvZoLl8sWifxpTLp93SE_3DOHAQFIpgGU4T1o1V4UwbOkHT6y8eVF8-h4CtTw6CJw==', 'gAAAAABjTYHhC0-jRRWVj-ddwIm_BjWO1SMXwAXC75QD3C_q-oiwAy4cUIRtwa738Z5NfgzzYw_0KSL41qJJqCa1_Kn-lzShgQ==', 'gAAAAABjTYHhgiZszbvd_Y_ZWE0Vi81ER6S4Do5c-n7hLUy2XOxFtngKuUm1sNotyCUfv9sS5y9jEbaBEqGDheXlkWluWuEa4b08oxDKxevqUTDQAVnaIMo=', 'gAAAAABjTYHhth4d8tWcAhTmHnwMMOfBgB1qkSHbnPUPgxpPOncShrCWwYQPljrsYKFzDcM-JInSq6eOSNOONJ6qs7DT4vp9PFhE84u5sqZMsGOz0q73QHo=', 'gAAAAABjTYHhDgleA3dqx1m_42b9qSvG-WJ4rHUQWqFeihHwDB36hDrqDx4Kuxcb0_5sMe1rcZQIAm5yayyJzTWa9Fepy9iAAA==', 'gAAAAABjTYHh_Y0A6M7tJFnESx1oKQt_-TyCWZlpKpS58JP7u1OaCaZmCsEJBfeSEcKuwCVQLmr5oOi16URi4K106AKZey4FYg==', 'gAAAAABjTYHhVr6ffkznx_ByQnTu6gXkOpJCN5MTd9V_v-yVEhZgPlJRQnRdek4cwmKYxy86rZnLeGMx_J8n9TW4LSIdA4o-2paoMRz1OEazsDwTx5bzjys=', 'gAAAAABjTYHhXuPSDOjtkRuMDfWxvp5mA10kPBN9_Emd9UCSzgDgdkVh3vgssIaHIKtcMLQUZONqdqF5OQn0FUrgbzZR6d3ToA==', 'gAAAAABjTYHhGYGGT2Uh0O53O3UFy1NhzhyYJdzbq2K7W-YIRlPyH6B8dtnKm7LcTDHSZWoEEN0IbmCTU4-iVN55hM7lBemEiQ==', 'gAAAAABjTYHhJ2WnXShm30dbIdF0s2eBOPJajvYv4uCJRHwgpaLZ4RKpV0amHRgX1LgItSsIEhe4ogYl9DYs_xg8b6JnkH_BBw==', 'gAAAAABjTYHhfaBP_5olr0ghUy51d37wEb22SuLpj7YJ6fm4kMOwQ_Fb-x6qnwFePTiTLDpgyAbDqbRrbpVv3sFa9EOY0X0Fxw==', 'gAAAAABjTYHhFbATPRZ21YC9hMq8oaRcFXMswMBs238JOZmy_PCbtTbv4pjwdxqFpNYUnx0VlszDpIN1p9mOPWc85TFZoRo9qg==', 'gAAAAABjTYHhFLCE8XqZyeNYWigUT4X9CgPec0zk0nyz6z-CCq2Fv7arMDtINBTEvHQHPE1couDzHqIyff8vB494hH_Ogx_FGA==', 'gAAAAABjTYHhifMb8a0Yw7Uph13O2-83ngmk-tdt6welEJ8jBjcM9mcMxTipk3P4ZSUWvUtIGTiMi65GK0dDn0XwhDigq99m1w==', 0, 1, 1),
(44, 2, 'DORSIMA s.r.o.', '04501616', 'CZ04501616', 'Táborská', '496', 'Písek', '39701', 'Česká republika', 'Krajský soud v Českých Budějovicích', 'C 24195', '', '', '', '', '', '', '', '', '', 1, 1, 0),
(45, 3, 'DORSIMA s.r.o.', '04501616', 'CZ04501616', 'Táborská', '496', 'Písek', '39701', 'Česká republika', 'Krajský soud v Českých Budějovicích', 'C 24195', '7033405508', 'zikavaclav05@gmail.com', 'zikav.eu', '2001587383', '2010', '', '', '', '', 0, 1, 0),
(46, 3, 'Alza.cz a.s.', '27082440', 'CZ27082440', 'Jankovcova', '1522', 'Praha', '17000', 'Česká republika', 'Městský soud v Praze', 'B 8573', '703340508', 'lol@email.cz', 'lol.cz', '2001587383', '2010', '12345678', 'asd123456', '123', '321', 0, 1, 0),
(47, 3, 'Alza.cz a.s.', '27082440', 'CZ27082440', 'Jankovcova', '1522', 'Praha', '17000', 'Česká republika', 'Městský soud v Praze', 'B 8573', '703340508', 'zika@email.cz', 'zikav.eu', '2001587383', '2010', '123456789', '', '123', '321', 1, 0, 0),
(48, 1, 'DORSIMA s.r.o.', '04501616', 'CZ04501616', 'Táborská', '496', 'Písek', '39701', 'Česká republika', 'Krajský soud v Českých Budějovicích', 'C 24195', '', '', '', '2001587383', '2010', '123456789', '789asd4564ads', '123', '654', 0, 1, 0),
(49, 1, 'Alza.cz a.s.', '27082440', 'CZ27082440', 'Jankovcova', '1522', 'Praha', '17000', 'Česká republika', 'Městský soud v Praze', 'B 8573', '', '', '', '2001587383', '2010', '', '', '', '', 0, 1, 0),
(50, 1, 'Příklad', '12345678', '12345678', 'Novákova', '32', 'Písek', '39701', 'Česko', 'Krajský soud v Českých Budějovicích', 'C 24195', '+420 702 504 598', 'priklad@seznam.cz', 'priklad', '88444422', '0800', '12345678', '12345678', '123', '321', 0, 1, 0),
(51, 1, 'Protipříklad', '98765432', '13456789', 'Příkladná', '123', 'Praha', '12345', 'Česko', 'vedeno v obchodním rejstříku, Městský soud v Praze, vložka C 92381', 'C 50506', '+420 506 652 123', 'protipriklad@seznam.cz', 'protipriklad.cz', '88444422', '0800', '12345678', '456', '123', '123', 1, 0, 0);

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
  `cena` tinytext NOT NULL,
  `mena` tinytext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `polozky`
--

INSERT INTO `polozky` (`id`, `user_id`, `faktura_id`, `dodavka`, `dph`, `pocet`, `cena`, `mena`) VALUES
(1, 1, 3, 'lmao', '12', '200', '21', 'usd'),
(2, 1, 4, 'Auto', '2', '200', '21', 'euro'),
(3, 2, 5, 'LOL', '20', '200', '21', 'euro'),
(4, 2, 6, 'LOL', '20', '200', '21', 'euro'),
(5, 2, 7, 'LOL', '20', '200', '21', 'euro'),
(6, 2, 8, 'asd', '123', '123', '123', '123'),
(7, 2, 9, 'asd', '123', '123', '123', '123'),
(8, 2, 0, 'asd', '789', '456', '46', '312'),
(9, 2, 0, '', '0', '0', '0', ''),
(10, 2, 10, 'asddsadsadsadsa', '123', '123', '132', '312'),
(11, 2, 0, 'asddsgfgdfdsgetwtwe', '456', '879', '321', 'dfsaadf'),
(12, 2, 0, '', '0', '0', '0', ''),
(13, 2, 11, 'asddsadsadsadsa', '123', '123', '132', '312'),
(14, 2, 0, 'asddsgfgdfdsgetwtwe', '456', '879', '321', 'dfsaadf'),
(15, 2, 12, 'asddsadsadsadsa', '123', '123', '132', '312'),
(16, 2, 0, 'asddsgfgdfdsgetwtwe', '456', '879', '321', 'dfsaadf'),
(17, 3, 13, 'Auto', '2', '20000', '21', 'usd'),
(18, 3, 0, 'Kolo', '1', '1500', '21', 'usd'),
(19, 3, 14, 'Bicykl', '2', '4500', '21', 'lol'),
(20, 3, 0, 'Program', '3', '1200', '21', 'lmao'),
(21, 3, 15, 'Bum', '2', '1500', '21', ''),
(22, 3, 15, 'Bac', '1', '13', '42', ''),
(23, 1, 17, 'asd', '123', '123', '123', '123'),
(24, 1, 18, 'dfsfds', '123', '123', '132', 'SDAF'),
(25, 1, 19, 'Auto', '21', '13', '21', 'usd'),
(26, 1, 19, 'kolo', '12', '123', '15', '456'),
(27, 1, 20, 'asddsa', '231', '32', '123', '123asd'),
(28, 1, 21, 'kappa', '210', '13123123', '21', 'usd'),
(29, 1, 21, 'lmao', '20', '123', '21', 'usd'),
(30, 1, 22, 'Auto', '2', '20000', '21', 'usd'),
(31, 1, 22, 'Bicykl', '3', '4200', '21', 'czk'),
(32, 1, 22, 'Pronájem domu', '4', '5000', '25', 'czk'),
(37, 1, 26, 'gAAAAABjVu8cQ1UHR_AGtL43sZ6EI1WRDzkaCcxmULRtA6-kkV8mJ1tuIZgmW0MSKCVWNt9AG2FGSy-T8RIx8pUSPpE340f-gA==', 'gAAAAABjVu8cggy9kBM80nyYwYgv4ZC4l4fJShLpT2D47cQgF4_-K0gpCgJ07jLp4WivuIq_T-_8eNtcKPSosw_ZHWr8jj_KMg==', 'gAAAAABjVu8czLK8cs1Ho6T7mxCzhG-T07TJWHM0ipHgvljXsIOzn6doG_WO5xUGt0UPWogZ39z5FFbt7Df4eUFP08bNlJhw6A==', 'gAAAAABjVu8cbtUYPKlzbhhMyIpjV1S1IP5H-JvjcKd1UfIyETT4DLRQM4KPijWPXiS-HZik1vcdEOtmKTtrr1QEyl-PtNarNg==', 'gAAAAABjVu8cybO0xCl2WQiYPGpQOyrey5u91e2aZottuGJ6xL22E5RuL-9UvkeHVOlxpHGTCmSJgfPIq383PiN9G8V31ALbcA=='),
(38, 1, 27, 'lol', '2', '200', '21', 'usd'),
(39, 1, 28, 'lol', '21', '2', '200', 'usd'),
(40, 1, 29, 'gAAAAABjVvAikhowNKJW2attuHalF4fAk0bdtR32uiiWRholR2Jsva1s1geRQR5UCyzJoXVPhbQLEzEfZCBA0RLFrjM_fs4fug==', 'gAAAAABjVvAiip8x09J3EyJoX13ca-Nkwf-prhFVTB5EBVHq2lem8WipphtBsg01goyxLi6XCC-2d0vSvxy9xKIy2s-DLAGTcw==', 'gAAAAABjVvAieD5nrbEn-bJc0lLm2hmepmoEiq6zs0ORA-4Ty6Ylu5qa2VYNyIWEMpp_zbdKGWd-k1hp52ZqTgEC6rc6laHN1g==', 'gAAAAABjVvAimmf5c-_ofv3q3Yhw06ojCrvur6cmummMrJsy0r-OjhtXNZl52ixNiuLTDLGj9_N8LbsCZiGvCDM9aVg6K7Ffeg==', 'gAAAAABjVvAiFgadotlXmReprq3W4TZwnNI3E9q3jEY9qSl7Tjo0ka1ma3HoVnrJBkEudE5FpydtVWS5YbZo_cL3qJ6AQKR8oA=='),
(41, 2, 30, 'asd', '123', '1132', '456', 'usd');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(256) NOT NULL,
  `password` varchar(2048) NOT NULL,
  `data_key` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `data_key`) VALUES
(1, 'Walter', '$2b$12$8U94VwOzU8GH6JUBhXQbE.A9xXKMUBoTEqoElXVNNKRJF/a2nEote', 'gAAAAABjQdDw_RGBvVLQkwKnhZNPBWY21_s90n3Ks750sG8dlwwdjf75NsW-x6PUYIMMmC2rgC_RSPa392LJx2qTrgfIlJ60I_4-HtDJuij8jFamXUGkCykVXYJTrBFnMKbdftpErgFX'),
(2, 'lol', '$2b$12$4CRugY4hloYrm2noke6BI.PLPuE2UDEHZabnAxy6.2SCyR.pQZlAO', 'gAAAAABjRw2efazR5BOjqbh_WTCUke6ZNoLKiyNoFLEIesF_-zCQDKmBNI-DwPyOSLrniha379Rpds-SLz0_MqmRuiupRNobRD9WZB6-csrkrXXx2Na3wuni875bKRIsx03TF_4zJnsm'),
(3, 'lmao', '$2b$12$0wBBon0/ug40p53VIsLUd.r6M2YfFGJkLkC4KJ0HvqikXbSVp8bSy', 'gAAAAABjUXTirTbrSaZPlmLLDKzr1Cp0HQjJ41978b3E-fvvgRJhJsWL91vHfBzR7v-GrYr2LdpjoGHM-FxVHeRX9duA_n4zCfFAIn7M_cFqUhCEBlbtv3pA1Zcmxlc_opzRkFfAlLzW');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `firmy`
--
ALTER TABLE `firmy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `polozky`
--
ALTER TABLE `polozky`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
