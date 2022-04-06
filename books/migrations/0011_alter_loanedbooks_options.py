from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_loanedbooks_point'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loanedbooks',
            options={'ordering': ['return_state'], 'verbose_name': '도서 대출', 'verbose_name_plural': '대출 도서 목록'},
        ),
    ]
