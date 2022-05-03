from django.db import models

# Create your models here.

class Order(models.Model):
    # on_delete는 fcuser가 삭제되었을 때 Order는 어떻게 처리 할 건지 관련된 속성, CASCADE는 같이 삭제되도록 한다.
    fcuser = models.ForeignKey('fcuser.Fcuser', on_delete=models.CASCADE,verbose_name='사용자') 
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.IntegerField(verbose_name='수량')
    status = models.CharField(
        # choice를 통해서 콤보박스 만들어줄 수 있음.
        choices=(
            ('대기중','대기중'),
            ('결제대기','결제대기'),
            ('결제완료','결제완료'),
            ('환불','환불'),
        ),
        default='대기중', max_length=32, verbose_name='상태'
        )
    memo = models.TextField(null=True, blank=True, verbose_name='메모')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return str(self.fcuser) + ' ' + str(self.product)

    class Meta:
        db_table = 'fastcampus_order'
        verbose_name = '주문'
        verbose_name_plural = '주문'
