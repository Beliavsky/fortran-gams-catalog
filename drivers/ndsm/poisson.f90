! BSD 3-Clause License
!
! Copyright (c) 2024, S.A. Gilchrist
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! 1. Redistributions of source code must retain the above copyright notice, this
!    list of conditions and the following disclaimer.
!
! 2. Redistributions in binary form must reproduce the above copyright notice,
!    this list of conditions and the following disclaimer in the documentation
!    and/or other materials provided with the distribution.
!
! 3. Neither the name of the copyright holder nor the names of its
!    contributors may be used to endorse or promote products derived from
!    this software without specific prior written permission.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
! DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
! FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
! DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
! SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
! OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
! OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
! GAMS I2b1a1a. Manufactured Neumann problem, following the author test setup.
program check_poisson
  use ndsm_root
  use ndsm_poisson
  implicit none
  real(fp) :: errors(2),residuals(2),gauges(2)
  debug=.false.
  call solve_case(17_it,25_it,3_it,errors(1),residuals(1),gauges(1))
  call solve_case(33_it,49_it,4_it,errors(2),residuals(2),gauges(2))
  if(.not.(errors(2)<0.35_fp*errors(1)))error stop 'refinement did not reduce error by expected order'
  print '(a,es12.4)','Fine/coarse error ratio: ',errors(2)/errors(1)
  print '(a)','PASS Poisson: two grids, analytic error, interior residual and zero-mean gauge'
contains
  subroutine solve_case(nx,ny,ng,error,residual,gauge)
    integer(it),intent(in) :: nx,ny,ng
    real(fp),intent(out) :: error,residual,gauge
    type(mg_ptr) :: mesh(2)
    type(mg_handle) :: bvp
    real(fp),allocatable :: u(:,:),exact(:,:),rhs(:,:)
    real(fp) :: h,x,y,lx,ly,du,stencil
    real(fp),parameter :: a=0.75_fp,b=-0.4_fp
    integer(it) :: nshape(2),nsize,ierr
    integer :: i,j
    nshape=[nx,ny]; nsize=nx*ny; h=1.0_fp/real(nx-1,fp)
    lx=1.0_fp; ly=real(ny-1,fp)*h
    allocate(mesh(1)%val(nx),mesh(2)%val(ny),u(nx,ny),exact(nx,ny),rhs(nx,ny))
    mesh(1)%val=[(real(i-1,fp)*h,i=1,int(nx))]
    mesh(2)%val=[(real(j-1,fp)*h,j=1,int(ny))]
    do j=1,int(ny)
      y=mesh(2)%val(j)
      do i=1,int(nx)
        x=mesh(1)%val(i)
        rhs(i,j)=a*(2*x-lx)+b*(2*y-ly)
        exact(i,j)=a*x*x*(x/3-lx/2)+b*y*y*(y/3-ly/2)
      enddo
    enddo
    exact=exact-sum(exact)/real(nsize,fp)
    call new_mg_handle(bvp,2_it,nshape,ng,mesh,.true.,100000_it)
    bvp%ms=5_it; bvp%ex_tol=1e-13_fp; bvp%copt='N'
    u=0.0_fp
    call solve_poisson_bvp(bvp,nsize,1e-12_fp,256_it,u,rhs,du,ierr)
    if(ierr/=IERR_POISSON_SUCCESS)error stop 'Poisson solver did not report convergence'
    error=maxval(abs(u-exact)); gauge=abs(sum(u)/real(nsize,fp)); residual=0.0_fp
    do j=2,int(ny)-1
      do i=2,int(nx)-1
        stencil=(u(i-1,j)+u(i+1,j)+u(i,j-1)+u(i,j+1)-4*u(i,j))/(h*h)
        residual=max(residual,abs(stencil-rhs(i,j)))
      enddo
    enddo
    if(.not.(error<0.5_fp*h*h))error stop 'analytic solution error too large'
    if(.not.(residual<5e-8_fp))error stop 'independent interior residual too large'
    if(.not.(gauge<1e-11_fp))error stop 'Neumann solution gauge not removed'
    print '(a,2i5,a,3es13.5)','Grid ',nx,ny,' error/residual/mean: ',error,residual,gauge
    call delete_mg_handle(bvp)
  end subroutine
end program check_poisson
