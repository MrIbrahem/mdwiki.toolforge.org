<?php

namespace TopIndex;
use function Functions\ColSm;
use function LeaderTables\NumbsTableNew;
use function LeaderTables\LangsTableNew;

if (isset($_GET['test']) || $_SERVER['SERVER_NAME'] == 'localhost') {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
};

function generateLeaderboardTable(): void
{
    $numbersTable = NumbsTableNew();
    $numbersCol   = ColSm('Numbers', $numbersTable);
    $cat = "Files_imported_from_NC_Commons";
    $languagesTable = LangsTableNew($cat);
    $languagesCol = ColSm('Languages', $languagesTable);

    echo <<<HTML
        <div class="container">
            <span align="center">
            </span>
            <div class="row">
                <div class="col-md-3">
                    $numbersCol
                </div>
                <div class="col-md-9">
                    $languagesCol
                </div>
            </div>
        </div>
    HTML;
}
