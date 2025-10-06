using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AMLService.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Analysis",
                columns: table => new
                {
                    AnalysisID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    UserID = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CreationDate = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Status = table.Column<string>(type: "nvarchar(max)", nullable: false, defaultValue: "Pending")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Analysis", x => x.AnalysisID);
                });

            migrationBuilder.CreateTable(
                name: "GeneratedDrug",
                columns: table => new
                {
                    GeneratedDrugID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    ProteinStructure = table.Column<byte[]>(type: "varbinary(max)", nullable: false),
                    CompletionDate = table.Column<DateTime>(type: "datetime2", nullable: false),
                    AnalysisID = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GeneratedDrug", x => x.GeneratedDrugID);
                    table.ForeignKey(
                        name: "FK_GeneratedDrug_Analysis_AnalysisID",
                        column: x => x.AnalysisID,
                        principalTable: "Analysis",
                        principalColumn: "AnalysisID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_GeneratedDrug_AnalysisID",
                table: "GeneratedDrug",
                column: "AnalysisID",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "GeneratedDrug");

            migrationBuilder.DropTable(
                name: "Analysis");
        }
    }
}
