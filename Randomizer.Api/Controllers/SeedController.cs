using System.Collections.Specialized;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Randomizer.Api.Configuration;
using Randomizer.Api.Extensions;
using Randomizer.Api.Handlers;

namespace Randomizer.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SeedController : ControllerBase
    {
        private readonly RandomizerHandler _randomizer;
        private readonly RandomizerConfiguration _configuration;

        public SeedController(RandomizerHandler randomizer, RandomizerConfiguration configuration)
        {
            _randomizer = randomizer;
            _configuration = configuration;
        }

        [HttpPost, RequestSizeLimit(3000000)]
        public async Task<IActionResult> GenerateAsync(CancellationToken cancellationToken)
        {
            var rom = Request.GetRomFileFromRequest();
            if (rom == null)
                return BadRequest("Failed to get ROM file from request");

            var seed = Request.GetSeedFromRequestOrDefault();
            var parameters = Request.GetParametersFromRequestOrDefault();

            var validHeader = rom.IsValidRomFile();
            if (!validHeader)
                return BadRequest("ROM file must be the US version of Illusion of Gaia");
            
            var uploadedFileDetails = await rom.CopyFileToTempStorageAsync(_configuration, cancellationToken);
            var randomizedFileDetails = await _randomizer.CreateRandomizedRomAsync(seed, uploadedFileDetails, parameters);
            
            if (!randomizedFileDetails.Success)
                return BadRequest(randomizedFileDetails.Error);

            using (var stream = await _randomizer.GetFileStreamAndDeleteRandomizedRomAsync(uploadedFileDetails, randomizedFileDetails.RomPath))
            {
                var disposition = new System.Net.Mime.ContentDisposition($"attachment;filename=\"{Path.GetFileName(randomizedFileDetails.RomPath)}\";seed=\"{seed}\";");

                Response.Headers.Add("Content-Disposition", disposition.ToString());
                Response.Headers.Add("X-Content-Type-Options", "nosniff");
                return File(stream.ToArray(), "application/octet-stream");
            }
        }

        [HttpGet, Route("{seed}/spoiler")]
        public async Task<IActionResult> DownloadSpoilerAsync(long seed, CancellationToken cancellationToken)
        {
            var file = _randomizer.GetSpoilerLog(seed);

            var stream = file.OpenRead();
            var disposition = new System.Net.Mime.ContentDisposition($"attachment;filename=\"{Path.GetFileName(file.Name)}\";");

            Response.Headers.Add("Content-Disposition", disposition.ToString());
            Response.Headers.Add("X-Content-Type-Options", "nosniff");
            return File(stream, "application/octet-stream");
        }
    }
}