using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AMLService.Migrations
{
    /// <inheritdoc />
    public partial class secondCreation : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_GeneratedDrug_Analysis_AnalysisID",
                table: "GeneratedDrug");

            migrationBuilder.DropPrimaryKey(
                name: "PK_GeneratedDrug",
                table: "GeneratedDrug");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Analysis",
                table: "Analysis");

            migrationBuilder.RenameTable(
                name: "GeneratedDrug",
                newName: "GeneratedDrugs");

            migrationBuilder.RenameTable(
                name: "Analysis",
                newName: "Analyses");

            migrationBuilder.RenameIndex(
                name: "IX_GeneratedDrug_AnalysisID",
                table: "GeneratedDrugs",
                newName: "IX_GeneratedDrugs_AnalysisID");

            migrationBuilder.AddPrimaryKey(
                name: "PK_GeneratedDrugs",
                table: "GeneratedDrugs",
                column: "GeneratedDrugID");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Analyses",
                table: "Analyses",
                column: "AnalysisID");

            migrationBuilder.AddForeignKey(
                name: "FK_GeneratedDrugs_Analyses_AnalysisID",
                table: "GeneratedDrugs",
                column: "AnalysisID",
                principalTable: "Analyses",
                principalColumn: "AnalysisID",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_GeneratedDrugs_Analyses_AnalysisID",
                table: "GeneratedDrugs");

            migrationBuilder.DropPrimaryKey(
                name: "PK_GeneratedDrugs",
                table: "GeneratedDrugs");

            migrationBuilder.DropPrimaryKey(
                name: "PK_Analyses",
                table: "Analyses");

            migrationBuilder.RenameTable(
                name: "GeneratedDrugs",
                newName: "GeneratedDrug");

            migrationBuilder.RenameTable(
                name: "Analyses",
                newName: "Analysis");

            migrationBuilder.RenameIndex(
                name: "IX_GeneratedDrugs_AnalysisID",
                table: "GeneratedDrug",
                newName: "IX_GeneratedDrug_AnalysisID");

            migrationBuilder.AddPrimaryKey(
                name: "PK_GeneratedDrug",
                table: "GeneratedDrug",
                column: "GeneratedDrugID");

            migrationBuilder.AddPrimaryKey(
                name: "PK_Analysis",
                table: "Analysis",
                column: "AnalysisID");

            migrationBuilder.AddForeignKey(
                name: "FK_GeneratedDrug_Analysis_AnalysisID",
                table: "GeneratedDrug",
                column: "AnalysisID",
                principalTable: "Analysis",
                principalColumn: "AnalysisID",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
