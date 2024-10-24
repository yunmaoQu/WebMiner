import pytest
from unittest.mock import patch, Mock
from src.notification.email_notifier import EmailNotifier
from src.utils.exceptions import NotificationException

@pytest.fixture
def notifier():
    return EmailNotifier()

@pytest.fixture
def sample_trending_data():
    return [
        ('test/repo1', 85.5, 1000, 500, 50, 'Python', 80.0),
        ('test/repo2', 75.5, 800, 400, 30, 'Java', 70.0),
    ]

def test_create_html_report(notifier, sample_trending_data):
    html_content = notifier._create_html_report(sample_trending_data)
    assert 'test/repo1' in html_content
    assert 'Python' in html_content
    assert '85.5' in html_content

@patch('smtplib.SMTP')
def test_send_trending_report(mock_smtp, notifier, sample_trending_data):
    mock_smtp_instance = Mock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    notifier.send_trending_report(sample_trending_data)
    
    assert mock_smtp_instance.starttls.called
    assert mock_smtp_instance.login.called
    assert mock_smtp_instance.send_message.called

@patch('smtplib.SMTP')
def test_send_trending_report_error(mock_smtp, notifier, sample_trending_data):
    mock_smtp.side_effect = Exception('SMTP error')
    
    with pytest.raises(NotificationException):
        notifier.send_trending_report(sample_trending_data)