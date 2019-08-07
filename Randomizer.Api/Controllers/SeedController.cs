using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Randomizer.Api.Extensions;
using Randomizer.Api.Handlers;

namespace Randomizer.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SeedController : ControllerBase
    {
        private readonly RandomizerHandler _randomizer;

        public SeedController(RandomizerHandler randomizer)
        {
            _randomizer = randomizer;
        }

        [HttpPost, RequestSizeLimit(3000000)]
        public async Task<IActionResult> GenerateAsync(CancellationToken cancellationToken)
        {
            var rom = Request.GetRomFileFromRequest();
            if (rom == null)
                return BadRequest();

            var seed = Request.GetSeedFromRequestOrDefault();
            var parameters = Request.GetParametersFromRequestOrDefault();

            var validHeader = rom.IsValidRomFile();
            if (!validHeader)
                return BadRequest("ROM file must be the US version of Illusion of Gaia");
            
            var uploadedFileDetails = await rom.CopyFileToTempStorageAsync(cancellationToken);
            var randomizedFileDetails = await _randomizer.CreateRandomizedRomAsync(seed, uploadedFileDetails, parameters);
            
            if (!randomizedFileDetails.Success)
                return BadRequest();
            
            var randomizedFile = new FileStream(randomizedFileDetails.RomPath, FileMode.Open, FileAccess.Read);
            var disposition = new System.Net.Mime.ContentDisposition
            {
                FileName = Path.GetFileName(randomizedFileDetails.RomPath),
                Inline = false
            };

            Response.Headers.Add("Content-Disposition", disposition.ToString());
            Response.Headers.Add("X-Content-Type-Options", "nosniff");
            
            return File(randomizedFile, "application/octet-stream");
        }
    }

    
}