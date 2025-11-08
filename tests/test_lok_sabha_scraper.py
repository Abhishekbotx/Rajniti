"""
Unit tests for Lok Sabha scraper.
"""

import pytest

from app.scrapers.lok_sabha import LokSabhaScraper


class TestLokSabhaScraper:
    """Test cases for LokSabhaScraper."""

    def test_scraper_initialization(self):
        """Test that the scraper initializes correctly."""
        url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
        scraper = LokSabhaScraper(url)

        assert scraper.base_url == "https://results.eci.gov.in/PcResultGenJune2024"
        assert scraper.year is None
        assert scraper.election_name is None
        assert scraper.folder_name is None
        assert scraper.parties_data == []
        assert scraper.constituencies_data == []
        assert scraper.candidates_data == []
        assert scraper.metadata == {}

    def test_generate_uuid(self):
        """Test that UUID generation works."""
        url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
        scraper = LokSabhaScraper(url)

        uuid1 = scraper._generate_uuid()
        uuid2 = scraper._generate_uuid()

        # UUIDs should be strings
        assert isinstance(uuid1, str)
        assert isinstance(uuid2, str)

        # UUIDs should be unique
        assert uuid1 != uuid2

        # UUIDs should have the correct format (contains hyphens)
        assert "-" in uuid1
        assert "-" in uuid2

    def test_generate_party_page_link(self):
        """Test party page link generation."""
        url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
        scraper = LokSabhaScraper(url)

        party_link = scraper._generate_party_page_link("369")

        expected = (
            "https://results.eci.gov.in/PcResultGenJune2024/"
            "partywisewinresultState-369.htm"
        )
        assert party_link == expected

    def test_generate_constituency_page_link(self):
        """Test constituency page link generation."""
        url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
        scraper = LokSabhaScraper(url)

        constituency_link = scraper._generate_constituency_page_link("S01", "5")

        expected = (
            "https://results.eci.gov.in/PcResultGenJune2024/"
            "candidateswise-S015.htm"
        )
        assert constituency_link == expected

    def test_extract_metadata(self):
        """Test metadata extraction from URL."""
        url = "https://results.eci.gov.in/PcResultGenJune2024/index.htm"
        scraper = LokSabhaScraper(url)

        scraper._extract_metadata()

        assert scraper.year == 2024
        assert scraper.election_name == "Lok Sabha General Election 2024"
        assert scraper.folder_name == "lok-sabha-2024"

    def test_extract_metadata_2019(self):
        """Test metadata extraction for 2019 election."""
        url = "https://results.eci.gov.in/PcResultGenJune2019/index.htm"
        scraper = LokSabhaScraper(url)

        scraper._extract_metadata()

        assert scraper.year == 2019
        assert scraper.election_name == "Lok Sabha General Election 2019"
        assert scraper.folder_name == "lok-sabha-2019"
