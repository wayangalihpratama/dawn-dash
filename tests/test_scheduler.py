from src.scheduler.service import MarketScheduler


def test_scheduler_add_jobs():
    scheduler = MarketScheduler()

    # Add dummy jobs
    def dummy():
        pass

    scheduler.add_signal_job(dummy, hour=15, minute=50)
    scheduler.add_journal_job(dummy, hour=17, minute=0)
    scheduler.add_exit_job(dummy, hour=9, minute=0)

    # Check jobs
    jobs = scheduler.scheduler.get_jobs()
    assert len(jobs) == 3

    job_names = [j.name for j in jobs]
    assert "BSJP_Signal_Scan" in job_names
    assert "Daily_Journal" in job_names
    assert "Automated_Exit" in job_names


def test_scheduler_timezone():
    scheduler = MarketScheduler(timezone="Asia/Jakarta")
    assert str(scheduler.tz) == "Asia/Jakarta"
